from django.contrib import admin

from .models import Attendance, Children


@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kana",
        "birthday",
        "gender",
        "facility_id",
        "class_id",
        "sub_class_id",
    )
    list_filter = ("gender", "class_id")
    search_fields = ("name", "kana", "class_id")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("date", "child", "is_absent", "reason")
    list_filter = ("date", "is_absent")
    search_fields = ("child__name", "child__kana", "child__class_id", "reason")
