from django.db import migrations, models


def forwards_split_name(apps, schema_editor):
    Staff = apps.get_model("nursery", "Staff")
    for staff in Staff.objects.all():
        legacy = (getattr(staff, "name", None) or "").strip()
        if not legacy:
            staff.last_name = ""
            staff.first_name = ""
        else:
            parts = legacy.split(None, 1)
            if len(parts) == 2:
                staff.last_name, staff.first_name = parts
            else:
                staff.last_name = legacy
                staff.first_name = ""
        staff.save(update_fields=["last_name", "first_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0012_children_split_kana"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="last_name",
            field=models.CharField(default="", max_length=50, verbose_name="姓"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="staff",
            name="first_name",
            field=models.CharField(default="", max_length=50, verbose_name="名"),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_split_name, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="staff",
            name="name",
        ),
        migrations.AlterModelOptions(
            name="staff",
            options={
                "ordering": ["facility_id", "kana", "last_name", "first_name"],
                "verbose_name": "スタッフ",
                "verbose_name_plural": "スタッフ",
            },
        ),
    ]
