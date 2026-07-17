from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ChildRegisterForm
from .models import Attendance, Children, Class


def _parse_class_filter(request):
    class_param = request.GET.get("class") or request.POST.get("class_filter")
    if not class_param or class_param == "all":
        return None
    try:
        return int(class_param)
    except (TypeError, ValueError):
        return None


def _build_child_list_context(class_id=None):
    children_list = Children.objects.select_related("nursery_class", "sub_class", "facility").all()
    if class_id is not None:
        children_list = children_list.filter(nursery_class_id=class_id)

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
        "classes": Class.objects.filter(is_deleted=False).order_by("id"),
        "selected_class_id": class_id,
        "today": today,
    }


def top_view(request):
    today = timezone.now().date()
    absent_children = Attendance.objects.filter(date=today, attendance_status=3).select_related(
        "child__nursery_class"
    )
    return render(
        request,
        "nursery/top.html",
        {"absent_children": absent_children, "today": today},
    )


def child_list_view(request):
    context = _build_child_list_context(class_id=_parse_class_filter(request))
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
            class_id = _parse_class_filter(request)
            if class_id is not None:
                return redirect(f"{reverse('child_list')}?class={class_id}")
            return redirect(reverse("child_list"))
    else:
        form = ChildRegisterForm()

    context = _build_child_list_context(class_id=_parse_class_filter(request))
    context["register_form"] = form
    return render(request, "nursery/child_list.html", context)


def absent_list_partial(request):
    today = timezone.now().date()
    absent_children = Attendance.objects.filter(date=today, attendance_status=3).select_related(
        "child__nursery_class"
    )
    return render(
        request,
        "nursery/partials/absent_list_partial.html",
        {"absent_children": absent_children},
    )


def child_detail_partial(request, child_id: int):
    child = get_object_or_404(
        Children.objects.select_related("facility", "nursery_class", "sub_class"),
        pk=child_id,
    )
    today = timezone.localdate()
    attendance = Attendance.objects.filter(child=child, date=today).first()
    parent_relationships = (
        child.parent_relationships.filter(is_deleted=False)
        .select_related("parent")
        .order_by("-is_main_contact", "relationship_type", "parent__kana")
    )
    return render(
        request,
        "nursery/partials/child_detail_partial.html",
        {
            "child": child,
            "attendance": attendance,
            "today": today,
            "parent_relationships": parent_relationships,
        },
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
    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(
        referer, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(referer)
    return redirect(reverse("child_list"))
