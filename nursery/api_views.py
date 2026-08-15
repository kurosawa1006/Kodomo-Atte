from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Attendance, Children, Parent, Staff
from .serializers import (
    AttendanceSerializer,
    ChildrenSerializer,
    ParentSerializer,
    StaffSerializer,
)


class ChildrenViewSet(viewsets.ReadOnlyModelViewSet):
    """園児一覧・詳細 API"""

    serializer_class = ChildrenSerializer
    queryset = Children.objects.filter(is_deleted=False).select_related(
        "facility",
        "nursery_class",
        "sub_class",
    )

    def get_queryset(self):
        qs = super().get_queryset()
        class_id = self.request.query_params.get("class")
        if class_id and class_id != "all":
            qs = qs.filter(nursery_class_id=class_id)
        facility_id = self.request.query_params.get("facility")
        if facility_id:
            qs = qs.filter(facility_id=facility_id)
        return qs


class StaffViewSet(viewsets.ReadOnlyModelViewSet):
    """スタッフ一覧・詳細 API"""

    serializer_class = StaffSerializer
    queryset = Staff.objects.filter(is_deleted=False).select_related("facility", "staff_role")


class ParentViewSet(viewsets.ReadOnlyModelViewSet):
    """保護者一覧・詳細 API"""

    serializer_class = ParentSerializer
    queryset = Parent.objects.filter(is_deleted=False).select_related("facility")


class AttendanceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    出欠 API
    - GET /api/v1/attendances/ … 本日（または date 指定）の出欠一覧
    - POST /api/v1/attendances/ … 保護者からの出欠登録
    - PATCH /api/v1/attendances/{id}/ … 出欠更新
    - POST /api/v1/attendances/{id}/confirm/ … スタッフ確認済
    """

    serializer_class = AttendanceSerializer
    http_method_names = ["get", "post", "patch", "put", "head", "options"]

    def get_queryset(self):
        qs = Attendance.objects.filter(is_deleted=False).select_related(
            "child",
            "child__facility",
            "child__nursery_class",
            "child__sub_class",
        )
        date_param = self.request.query_params.get("date")
        if date_param:
            qs = qs.filter(date=date_param)
        else:
            qs = qs.filter(date=timezone.localdate())

        class_id = self.request.query_params.get("class")
        if class_id and class_id != "all":
            qs = qs.filter(child__nursery_class_id=class_id)

        confirmed = self.request.query_params.get("is_confirmed")
        if confirmed is not None:
            qs = qs.filter(is_confirmed=confirmed.lower() in {"1", "true", "yes"})

        status_param = self.request.query_params.get("attendance_status")
        if status_param:
            qs = qs.filter(attendance_status=status_param)

        return qs

    def perform_create(self, serializer):
        serializer.save(is_confirmed=False, is_deleted=False)

    def create(self, request, *args, **kwargs):
        """同一園児・同一日があれば更新（upsert）する。"""
        child_id = request.data.get("child")
        date_value = request.data.get("date") or timezone.localdate().isoformat()
        existing = Attendance.objects.filter(child_id=child_id, date=date_value).first()
        if existing:
            serializer = self.get_serializer(existing, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(is_confirmed=False, is_deleted=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        attendance = self.get_object()
        attendance.is_confirmed = True
        attendance.save(update_fields=["is_confirmed", "updated_at"])
        serializer = self.get_serializer(attendance)
        return Response(serializer.data)


class MeAPIView(APIView):
    """
    現在のユーザープロファイルを返す。

    認証導入前の暫定仕様:
    - Query: ?role=parent|staff&id=<pk>
    - または Header: X-Role / X-Profile-Id
    """

    def get(self, request):
        role = (
            request.query_params.get("role")
            or request.headers.get("X-Role")
            or ""
        ).strip().lower()
        profile_id = (
            request.query_params.get("id")
            or request.headers.get("X-Profile-Id")
            or ""
        ).strip()

        if role not in {"parent", "staff"}:
            return Response(
                {
                    "detail": "role に parent または staff を指定してください。",
                    "example": "/api/v1/me/?role=parent&id=1",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not profile_id.isdigit():
            return Response(
                {"detail": "id（または X-Profile-Id）に数値のプロファイル ID を指定してください。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if role == "parent":
            parent = Parent.objects.filter(pk=int(profile_id), is_deleted=False).first()
            if parent is None:
                return Response({"detail": "保護者が見つかりません。"}, status=status.HTTP_404_NOT_FOUND)
            children = Children.objects.filter(
                is_deleted=False,
                parent_relationships__parent=parent,
                parent_relationships__is_deleted=False,
            ).select_related("nursery_class", "sub_class").distinct()
            return Response(
                {
                    "role": "parent",
                    "permissions": ["attendance:create", "attendance:update", "children:read"],
                    "profile": ParentSerializer(parent).data,
                    "children": ChildrenSerializer(children, many=True).data,
                }
            )

        staff = Staff.objects.filter(pk=int(profile_id), is_deleted=False).select_related("staff_role").first()
        if staff is None:
            return Response({"detail": "スタッフが見つかりません。"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "role": "staff",
                "permissions": [
                    "attendance:read",
                    "attendance:confirm",
                    "children:read",
                    "staff:read",
                ],
                "profile": StaffSerializer(staff).data,
            }
        )
