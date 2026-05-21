from django import forms
from django.forms import ModelForm

from .models import Children, Class, Facility, SubClass


class ChildRegisterForm(ModelForm):
    class Meta:
        model = Children
        fields = [
            "name",
            "kana",
            "birthday",
            "gender",
            "facility",
            "nursery_class",
            "sub_class",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "kana": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "birthday": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "facility": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "nursery_class": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "sub_class": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        facilities = Facility.objects.filter(is_active=True).order_by("name", "id")
        self.fields["facility"].queryset = facilities
        if not self.fields["facility"].initial:
            self.fields["facility"].initial = (
                Facility.objects.filter(pk=1, is_active=True).first() or facilities.first()
            )

        classes = Class.objects.select_related("facility").order_by("facility_id", "name", "id")
        self.fields["nursery_class"].queryset = classes
        if not self.fields["nursery_class"].initial:
            self.fields["nursery_class"].initial = (
                Class.objects.filter(pk=1).first() or classes.first()
            )

        sub_classes = SubClass.objects.select_related("facility", "nursery_class").order_by(
            "facility_id", "nursery_class_id", "name", "id"
        )
        self.fields["sub_class"].queryset = sub_classes
        self.fields["sub_class"].required = False
