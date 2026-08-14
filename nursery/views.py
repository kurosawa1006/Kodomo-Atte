from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ChildRegisterForm
from .models import Attendance, Children, Class, Parent


CLASS_AGE_LABELS = {
    1: "0歳",
    2: "1歳",
    3: "2歳",
    4: "3歳",
    5: "4歳",
    6: "5歳",
}


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
    parent_ids = list(parent_relationships.values_list("parent_id", flat=True))
    siblings = (
        Children.objects.filter(
            is_deleted=False,
            parent_relationships__is_deleted=False,
            parent_relationships__parent_id__in=parent_ids,
        )
        .exclude(pk=child.pk)
        .select_related("nursery_class", "sub_class")
        .distinct()
        .order_by("nursery_class_id", "last_name_kana", "first_name_kana")
    )
    return render(
        request,
        "nursery/partials/child_detail_partial.html",
        {
            "child": child,
            "attendance": attendance,
            "today": today,
            "parent_relationships": parent_relationships,
            "siblings": siblings,
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
        obj.is_confirmed = False

    if existing:
        is_active = existing.attendance_status == attendance_code
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
            is_confirmed=False,
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


def staff_dashboard_view(request):
    today = timezone.localdate()
    class_id = _parse_class_filter(request)

    children_qs = Children.objects.filter(is_deleted=False)
    if class_id is not None:
        children_qs = children_qs.filter(nursery_class_id=class_id)
    total_children = children_qs.count()

    attendance_qs = Attendance.objects.filter(
        date=today,
        is_deleted=False,
        attendance_status__in=[
            Attendance.AttendanceStatus.LATE,
            Attendance.AttendanceStatus.EARLY_LEAVE,
            Attendance.AttendanceStatus.ABSENT,
        ],
    ).select_related("child", "child__nursery_class", "child__sub_class")
    if class_id is not None:
        attendance_qs = attendance_qs.filter(child__nursery_class_id=class_id)

    late_count = attendance_qs.filter(attendance_status=Attendance.AttendanceStatus.LATE).count()
    absent_count = attendance_qs.filter(attendance_status=Attendance.AttendanceStatus.ABSENT).count()
    present_count = max(total_children - late_count - absent_count, 0)

    unconfirmed_list = attendance_qs.filter(is_confirmed=False).order_by(
        "attendance_status",
        "child__last_name_kana",
        "child__first_name_kana",
    )

    class_tabs = [
        {
            "id": c.id,
            "name": c.name,
            "age_label": CLASS_AGE_LABELS.get(c.id, c.name),
        }
        for c in Class.objects.filter(is_deleted=False).order_by("id")
    ]

    return render(
        request,
        "staff/dashboard.html",
        {
            "today": today,
            "total_children": total_children,
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "unconfirmed_list": unconfirmed_list,
            "class_tabs": class_tabs,
            "selected_class_id": class_id,
        },
    )


@require_POST
def staff_confirm_attendance(request, attendance_id: int):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    attendance.is_confirmed = True
    attendance.save(update_fields=["is_confirmed", "updated_at"])
    messages.success(request, f"{attendance.child.full_name}さんの連絡を確認済みにしました")

    class_id = _parse_class_filter(request)
    if class_id is not None:
        return redirect(f"{reverse('staff_dashboard')}?class={class_id}")
    return redirect(reverse("staff_dashboard"))


def parent_dashboard_view(request):
    today = timezone.localdate()
    parent_id = request.GET.get("parent")
    parent = None
    if parent_id:
        parent = Parent.objects.filter(pk=parent_id, is_deleted=False).first()
    if parent is None:
        parent = (
            Parent.objects.filter(is_deleted=False, child_relationships__is_deleted=False)
            .order_by("id")
            .first()
        )

    child = None
    today_attendance = None
    if parent:
        rel = (
            parent.child_relationships.filter(is_deleted=False)
            .select_related("child", "child__nursery_class", "child__sub_class")
            .order_by("-is_main_contact", "child__last_name_kana")
            .first()
        )
        if rel:
            child = rel.child
            today_attendance = Attendance.objects.filter(child=child, date=today).first()

    notices = [
        {
            "title": "本日の持ち物について",
            "date": today.strftime("%m/%d"),
            "body": "気温の変動があります。着替えとタオルを多めにお願いします。",
        },
        {
            "title": "給食のお知らせ",
            "date": today.strftime("%m/%d"),
            "body": "本日の給食はカレーライスです。アレルギー対応もご用意しています。",
        },
    ]

    return render(
        request,
        "parent/dashboard.html",
        {
            "today": today,
            "parent": parent,
            "child": child,
            "today_attendance": today_attendance,
            "notices": notices,
        },
    )


@require_POST
def parent_report_attendance(request):
    parent_id = request.POST.get("parent_id")
    child_id = request.POST.get("child_id")
    parent = get_object_or_404(Parent, pk=parent_id, is_deleted=False)
    child = get_object_or_404(Children, pk=child_id, is_deleted=False)

    linked = parent.child_relationships.filter(child=child, is_deleted=False).exists()
    if not linked:
        messages.error(request, "この園児への連絡権限がありません")
        return redirect(f"{reverse('parent_dashboard')}?parent={parent.id}")

    status_to_code = {"late": 1, "early_leave": 2, "absent": 3}
    attendance_code = status_to_code.get(
        (request.POST.get("attendance_status") or "absent").strip(), 3
    )
    reason = (request.POST.get("reason") or "").strip()
    today = timezone.localdate()

    attendance, _created = Attendance.objects.update_or_create(
        child=child,
        date=today,
        defaults={
            "attendance_status": attendance_code,
            "reason": reason,
            "is_confirmed": False,
            "is_deleted": False,
        },
    )
    label = dict(Attendance.AttendanceStatus.choices).get(attendance.attendance_status, "連絡")
    messages.success(request, f"{child.full_name}さんの{label}連絡を送信しました")
    return redirect(f"{reverse('parent_dashboard')}?parent={parent.id}")
