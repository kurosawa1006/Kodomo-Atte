import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0002_class"),
    ]

    operations = [
        migrations.CreateModel(
            name="SubClass",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="サブクラス名")),
                ("description", models.TextField(blank=True, default="", verbose_name="説明")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "facility",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sub_classes",
                        to="nursery.facility",
                        verbose_name="施設ID",
                    ),
                ),
                (
                    "nursery_class",
                    models.ForeignKey(
                        db_column="class_id",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sub_classes",
                        to="nursery.class",
                        verbose_name="クラスID",
                    ),
                ),
            ],
            options={
                "verbose_name": "サブクラス",
                "verbose_name_plural": "サブクラス",
                "db_table": "sub_class",
                "ordering": ["facility_id", "nursery_class_id", "name", "id"],
            },
        ),
    ]
