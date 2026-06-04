from django.contrib import admin

from .models import (
    Attendance,
    Children,
    Class,
    SubClass,
    Facility,
    Parent,
    ParentChildRelationship,
    Staff,
    StaffRole,
)


@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "last_name_kana",
        "first_name_kana",
        "birthday",
        "gender",
        "facility",
        "nursery_class",
        "sub_class",
    )
    list_filter = ("gender", "nursery_class", "sub_class", "facility")
    search_fields = (
        "last_name",
        "first_name",
        "last_name_kana",
        "first_name_kana",
        "nursery_class__name",
        "sub_class__name",
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "child", "attendance_status", "reason")
    list_filter = ("date", "attendance_status")
    search_fields = (
        "child__last_name",
        "child__first_name",
        "child__last_name_kana",
        "child__first_name_kana",
        "child__nursery_class__name",
        "reason",
    )


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("id", "facility", "name", "description", "is_deleted", "created_at", "updated_at")
    list_filter = ("facility", "is_deleted")
    search_fields = ("name", "description", "facility__name")


@admin.register(SubClass)
class SubClassAdmin(admin.ModelAdmin):
    list_display = ("id", "facility", "nursery_class", "name", "description", "is_deleted", "created_at", "updated_at")
    list_filter = ("facility", "nursery_class", "is_deleted")
    search_fields = ("name", "description", "facility__name", "nursery_class__name")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "postal_code",
        "address",
        "phone_number",
        "capacity",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active", "is_deleted")
    search_fields = ("name", "postal_code", "address")


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "facility",
        "name",
        "kana",
        "phone_number",
        "emergency_contact",
        "postal_code",
        "address",
    )
    list_filter = ("facility",)
    search_fields = ("id", "name", "kana", "phone_number", "postal_code", "address", "facility__name")


@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_deleted", "created_at", "updated_at")
    list_filter = ("is_deleted",)
    search_fields = ("id", "name")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "facility",
        "staff_number",
        "staff_role",
        "last_name",
        "first_name",
        "last_name_kana",
        "first_name_kana",
        "phone_number",
        "postal_code",
        "address",
    )
    list_filter = ("facility", "staff_role")
    search_fields = (
        "id",
        "staff_number",
        "last_name",
        "first_name",
        "last_name_kana",
        "first_name_kana",
        "phone_number",
        "postal_code",
        "address",
        "staff_role__name",
        "facility__name",
    )


@admin.register(ParentChildRelationship)
class ParentChildRelationshipAdmin(admin.ModelAdmin):
    list_display = ("parent", "child", "relationship_type", "is_main_contact", "created_at")
    list_filter = ("relationship_type", "is_main_contact", "created_at")
    search_fields = (
        "parent__name",
        "parent__kana",
        "child__last_name",
        "child__first_name",
        "child__last_name_kana",
        "child__first_name_kana",
        "relationship_type",
    )
