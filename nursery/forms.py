from django import forms
from django.forms import ModelForm

from .models import Children, Class, Facility, SubClass

INPUT_CLASS = (
    "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm "
    "focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
)


class ChildRegisterForm(ModelForm):
    class Meta:
        model = Children
        fields = [
            "last_name",
            "first_name",
            "last_name_kana",
            "first_name_kana",
            "birthday",
            "gender",
            "facility",
            "nursery_class",
            "sub_class",
        ]
        widgets = {
            "last_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "first_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "last_name_kana": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "first_name_kana": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "birthday": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "gender": forms.Select(attrs={"class": INPUT_CLASS}),
            "facility": forms.Select(attrs={"class": INPUT_CLASS}),
            "nursery_class": forms.Select(attrs={"class": INPUT_CLASS}),
            "sub_class": forms.Select(attrs={"class": INPUT_CLASS}),
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
