from django.urls import path

from . import views

urlpatterns = [
    path("", views.top_view, name="top"),
    path(
        "absent-list-partial/",
        views.absent_list_partial,
        name="absent_list_partial",
    ),
    path("children/", views.child_list_view, name="child_list"),
    path(
        "children/register/",
        views.child_register_view,
        name="child_register",
    ),
    path(
        "children/<int:child_id>/toggle-attendance/",
        views.toggle_attendance,
        name="toggle_attendance",
    ),
    path(
        "children/<int:child_id>/detail/",
        views.child_detail_partial,
        name="child_detail",
    ),
    path("staff/dashboard/", views.staff_dashboard_view, name="staff_dashboard"),
    path(
        "staff/attendance/<int:attendance_id>/confirm/",
        views.staff_confirm_attendance,
        name="staff_confirm_attendance",
    ),
    path("parent/dashboard/", views.parent_dashboard_view, name="parent_dashboard"),
    path(
        "parent/report-attendance/",
        views.parent_report_attendance,
        name="parent_report_attendance",
    ),
]
