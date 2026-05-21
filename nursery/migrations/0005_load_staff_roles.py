from django.db import migrations

STAFF_ROLE_NAMES = [
    "施設長",
    "主任保育士",
    "副主任保育士",
    "リーダー保育士",
    "一般保育士",
    "パート・アルバイト保育士",
    "保育補助",
    "管理栄養士",
    "栄養士",
    "調理スタッフ",
    "看護師",
    "事務員",
]


def forwards_load_staff_roles(apps, schema_editor):
    StaffRole = apps.get_model("nursery", "StaffRole")
    for name in STAFF_ROLE_NAMES:
        StaffRole.objects.get_or_create(name=name)


def backwards_remove_staff_roles(apps, schema_editor):
    StaffRole = apps.get_model("nursery", "StaffRole")
    StaffRole.objects.filter(name__in=STAFF_ROLE_NAMES).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0004_staffrole"),
    ]

    operations = [
        migrations.RunPython(forwards_load_staff_roles, backwards_remove_staff_roles),
    ]
