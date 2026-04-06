from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ChildRegisterForm
from .models import Attendance, Children


def _build_child_list_context():
    children_list = Children.objects.all()
    today = timezone.localdate()
    attendance_today = (
        Attendance.objects.filter(date=today)
        .select_related("child")
        .only("id", "child_id", "attendance_status", "reason")
    )
    attendance_by_child_id = {a.child_id: a for a in attendance_today}
    rows = [{"child": c, "attendance": attendance_by_child_id.get(c.id)} for c in children_list]

    return {
        "rows": rows,
        "today": today,
    }


def top_view(request):
    today = timezone.now().date()
    absent_children = Attendance.objects.filter(date=today, attendance_status=3).select_related("child")
    return render(
        request,
        "nursery/top.html",
        {"absent_children": absent_children, "today": today},
    )


def child_list_view(request):
    context = _build_child_list_context()
    context["register_form"] = ChildRegisterForm()
    return render(
        request,
        "nursery/child_list.html",
        context,
    )


def child_register_view(request):
    if request.method == "POST":
        form = ChildRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("child_list"))
    else:
        form = ChildRegisterForm()

    context = _build_child_list_context()
    context["register_form"] = form
    return render(request, "nursery/child_list.html", context)


def absent_list_partial(request):
    today = timezone.now().date()
    absent_children = Attendance.objects.filter(date=today, attendance_status=3).select_related("child")
    return render(
        request,
        "nursery/partials/absent_list_partial.html",
        {"absent_children": absent_children},
    )


@require_POST
def toggle_attendance(request, child_id: int):
    child = get_object_or_404(Children, pk=child_id)
    today = timezone.localdate()
    attendance_status = (request.POST.get("attendance_status") or "absent").strip()
    status_to_code = {"late": 1, "early_leave": 2, "absent": 3}
    attendance_code = status_to_code.get(attendance_status, 3)

    reason = (request.POST.get("reason") or "").strip()
    existing = Attendance.objects.filter(child=child, date=today).first()

    def apply_status_to_obj(obj):
        obj.attendance_status = attendance_code
        obj.reason = reason

    if existing:
        is_active = (
            existing.attendance_status == attendance_code
        )
        if is_active:
            existing.delete()
        else:
            apply_status_to_obj(existing)
            existing.save()
    else:
        Attendance.objects.create(
            child=child,
            date=today,
            attendance_status=attendance_code,
            reason=reason,
        )
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect(reverse("child_list"))
