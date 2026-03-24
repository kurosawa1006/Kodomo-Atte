from django.contrib import admin

from .models import Children


@admin.register(Children)
class ChildrenAdmin(admin.ModelAdmin):
    list_display = ("name", "kana", "birthday", "gender", "classroom")
    list_filter = ("gender", "classroom")
    search_fields = ("name", "kana", "classroom")
