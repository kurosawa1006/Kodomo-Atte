from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Attendance, Children


def top_view(request):
    today = timezone.localdate()
    absent_attendances = Attendance.objects.filter(date=today, is_absent=True).select_related(
        "child"
    )
    return render(
        request,
        "nursery/top.html",
        {"absent_attendances": absent_attendances, "today": today},
    )


def child_list_view(request):
    children_list = Children.objects.all()
    today = timezone.localdate()
    absent_today = (
        Attendance.objects.filter(date=today, is_absent=True)
        .select_related("child")
        .only("id", "child_id", "reason")
    )
    absent_by_child_id = {a.child_id: a for a in absent_today}

    rows = [{"child": c, "attendance": absent_by_child_id.get(c.id)} for c in children_list]
    return render(
        request,
        "nursery/child_list.html",
        {"rows": rows, "today": today},
    )


@require_POST
def toggle_attendance(request, child_id: int):
    child = get_object_or_404(Children, pk=child_id)
    today = timezone.localdate()
    existing = Attendance.objects.filter(child=child, date=today, is_absent=True).first()
    if existing:
        existing.delete()
    else:
        reason = (request.POST.get("reason") or "").strip()
        Attendance.objects.create(child=child, date=today, is_absent=True, reason=reason)
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect(reverse("child_list"))
