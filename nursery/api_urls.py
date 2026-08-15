from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    AttendanceViewSet,
    ChildrenViewSet,
    MeAPIView,
    ParentViewSet,
    StaffViewSet,
)

router = DefaultRouter()
router.register(r"children", ChildrenViewSet, basename="api-children")
router.register(r"staff", StaffViewSet, basename="api-staff")
router.register(r"parents", ParentViewSet, basename="api-parents")
router.register(r"attendances", AttendanceViewSet, basename="api-attendances")

urlpatterns = [
    path("me/", MeAPIView.as_view(), name="api-me"),
    path("", include(router.urls)),
]
