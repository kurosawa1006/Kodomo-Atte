import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0009_attendance"),
    ]

    operations = [
        migrations.CreateModel(
            name="ParentChildRelationship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("relationship_type", models.CharField(max_length=50, verbose_name="続柄")),
                ("is_main_contact", models.BooleanField(default=False, verbose_name="主連絡先")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "child",
                    models.ForeignKey(
                        db_column="children_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parent_relationships",
                        to="nursery.children",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        db_column="parent_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child_relationships",
                        to="nursery.parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "保護者-園児リレーション",
                "verbose_name_plural": "保護者-園児リレーション",
                "db_table": "parent_child_relationships",
                "ordering": ["-created_at", "child__kana", "parent__kana"],
            },
        ),
    ]
