from django.urls import path

from . import views

urlpatterns = [
    path("", views.top_view, name="top"),
    path("children/", views.child_list_view, name="child_list"),
    path(
        "children/<int:child_id>/toggle-attendance/",
        views.toggle_attendance,
        name="toggle_attendance",
    ),
]
