from django.db import migrations, models


def forwards_split_kana(apps, schema_editor):
    Staff = apps.get_model("nursery", "Staff")
    for staff in Staff.objects.all():
        legacy = (getattr(staff, "kana", None) or "").strip()
        if not legacy:
            staff.last_name_kana = ""
            staff.first_name_kana = ""
        else:
            parts = legacy.split(None, 1)
            if len(parts) == 2:
                staff.last_name_kana, staff.first_name_kana = parts
            else:
                staff.last_name_kana = legacy
                staff.first_name_kana = ""
        staff.save(update_fields=["last_name_kana", "first_name_kana"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0013_staff_split_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="last_name_kana",
            field=models.CharField(default="", max_length=50, verbose_name="姓（かな）"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staff",
            name="first_name_kana",
            field=models.CharField(default="", max_length=50, verbose_name="名（かな）"),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_split_kana, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="staff",
            name="kana",
        ),
        migrations.AlterModelOptions(
            name="staff",
            options={
                "ordering": [
                    "facility_id",
                    "last_name_kana",
                    "first_name_kana",
                    "last_name",
                    "first_name",
                ],
                "verbose_name": "スタッフ",
                "verbose_name_plural": "スタッフ",
            },
        ),
    ]
