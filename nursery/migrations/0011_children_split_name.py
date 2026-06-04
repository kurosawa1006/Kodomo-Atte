from django.db import migrations, models


def forwards_split_name(apps, schema_editor):
    Children = apps.get_model("nursery", "Children")
    for child in Children.objects.all():
        legacy = (getattr(child, "name", None) or "").strip()
        if not legacy:
            child.last_name = ""
            child.first_name = ""
        else:
            parts = legacy.split(None, 1)
            if len(parts) == 2:
                child.last_name, child.first_name = parts
            else:
                child.last_name = legacy
                child.first_name = ""
        child.save(update_fields=["last_name", "first_name"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0010_parent_child_relationship"),
    ]

    operations = [
        migrations.AddField(
            model_name="children",
            name="last_name",
            field=models.CharField(default="", max_length=50, verbose_name="姓"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="children",
            name="first_name",
            field=models.CharField(default="", max_length=50, verbose_name="名"),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_split_name, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="children",
            name="name",
        ),
        migrations.AlterModelOptions(
            name="children",
            options={
                "ordering": ["nursery_class_id", "kana", "last_name", "first_name"],
                "verbose_name": "園児",
                "verbose_name_plural": "園児",
            },
        ),
        migrations.AlterModelOptions(
            name="attendance",
            options={
                "ordering": ["-date", "child__nursery_class_id", "child__kana", "child__last_name", "child__first_name"],
                "verbose_name": "出席",
                "verbose_name_plural": "出席",
            },
        ),
    ]
