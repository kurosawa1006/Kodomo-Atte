from django import forms
from django.forms import ModelForm

from .models import Children


class ChildRegisterForm(ModelForm):
    class Meta:
        model = Children
        fields = [
            "name",
            "kana",
            "birthday",
            "gender",
            "facility_id",
            "class_id",
            "sub_class_id",
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
            "facility_id": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "class_id": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
            "sub_class_id": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white/90 px-4 py-2 text-sm shadow-sm focus:outline-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # モデルのデフォルト値を、画面表示時にも入れて入力負担を下げる
        self.fields["facility_id"].initial = self.fields["facility_id"].initial or "1"
        self.fields["class_id"].initial = self.fields["class_id"].initial or "1"

