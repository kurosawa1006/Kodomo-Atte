import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0001_facility"),
    ]

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="クラス名")),
                ("description", models.TextField(blank=True, default="", verbose_name="説明")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="classes",
                        to="nursery.facility",
                        verbose_name="施設ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "クラス",
                "verbose_name_plural": "クラス",
                "db_table": "class",
                "ordering": ["facility_id", "name", "id"],
            },
        ),
    ]
