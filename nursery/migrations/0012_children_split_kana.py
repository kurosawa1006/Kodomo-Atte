from django.db import migrations, models


def forwards_split_kana(apps, schema_editor):
    Children = apps.get_model("nursery", "Children")
    for child in Children.objects.all():
        legacy = (getattr(child, "kana", None) or "").strip()
        if not legacy:
            child.last_name_kana = ""
            child.first_name_kana = ""
        else:
            parts = legacy.split(None, 1)
            if len(parts) == 2:
                child.last_name_kana, child.first_name_kana = parts
            else:
                child.last_name_kana = legacy
                child.first_name_kana = ""
        child.save(update_fields=["last_name_kana", "first_name_kana"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0011_children_split_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="children",
            name="last_name_kana",
            field=models.CharField(default="", max_length=50, verbose_name="姓（かな）"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="children",
            name="first_name_kana",
            field=models.CharField(default="", max_length=50, verbose_name="名（かな）"),
            preserve_default=False,
        ),
        migrations.RunPython(forwards_split_kana, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="children",
            name="kana",
        ),
        migrations.AlterModelOptions(
            name="children",
            options={
                "ordering": ["nursery_class_id", "last_name_kana", "first_name_kana", "last_name", "first_name"],
                "verbose_name": "園児",
                "verbose_name_plural": "園児",
            },
        ),
        migrations.AlterModelOptions(
            name="attendance",
            options={
                "ordering": [
                    "-date",
                    "child__nursery_class_id",
                    "child__last_name_kana",
                    "child__first_name_kana",
                    "child__last_name",
                    "child__first_name",
                ],
                "verbose_name": "出席",
                "verbose_name_plural": "出席",
            },
        ),
        migrations.AlterModelOptions(
            name="parentchildrelationship",
            options={
                "ordering": ["-created_at", "child__last_name_kana", "child__first_name_kana", "parent__kana"],
                "verbose_name": "保護者-園児リレーション",
                "verbose_name_plural": "保護者-園児リレーション",
            },
        ),
    ]
