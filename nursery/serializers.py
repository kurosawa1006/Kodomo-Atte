from rest_framework import serializers

from .models import Attendance, Children, Class, Parent, Staff, StaffRole, SubClass


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["id", "name", "description", "facility", "is_deleted"]


class SubClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubClass
        fields = ["id", "name", "description", "facility", "nursery_class", "is_deleted"]


class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ["id", "name", "is_deleted"]


class ChildrenSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    full_kana = serializers.CharField(read_only=True)
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)
    nursery_class_detail = ClassSerializer(source="nursery_class", read_only=True)
    sub_class_detail = SubClassSerializer(source="sub_class", read_only=True)

    class Meta:
        model = Children
        fields = [
            "id",
            "last_name",
            "first_name",
            "last_name_kana",
            "first_name_kana",
            "full_name",
            "full_kana",
            "birthday",
            "gender",
            "gender_display",
            "facility",
            "nursery_class",
            "nursery_class_detail",
            "sub_class",
            "sub_class_detail",
            "start_date",
            "end_date",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class StaffSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    full_kana = serializers.CharField(read_only=True)
    staff_role_detail = StaffRoleSerializer(source="staff_role", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "facility",
            "staff_number",
            "staff_role",
            "staff_role_detail",
            "last_name",
            "first_name",
            "last_name_kana",
            "first_name_kana",
            "full_name",
            "full_kana",
            "phone_number",
            "postal_code",
            "address",
            "start_date",
            "end_date",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = [
            "id",
            "facility",
            "name",
            "kana",
            "phone_number",
            "emergency_contact",
            "postal_code",
            "address",
            "start_date",
            "end_date",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class AttendanceSerializer(serializers.ModelSerializer):
    child_detail = ChildrenSerializer(source="child", read_only=True)
    attendance_status_display = serializers.CharField(
        source="get_attendance_status_display",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "child",
            "child_detail",
            "date",
            "attendance_status",
            "attendance_status_display",
            "reason",
            "scheduled_arrival_time",
            "note",
            "is_confirmed",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
