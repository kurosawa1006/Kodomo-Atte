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
]
