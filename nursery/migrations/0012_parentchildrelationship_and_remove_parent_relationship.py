from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0011_parent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="parent",
            name="relationship",
        ),
        migrations.CreateModel(
            name="ParentChildRelationship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("relationship_type", models.CharField(max_length=50, verbose_name="続柄")),
                ("is_main_contact", models.BooleanField(default=False, verbose_name="主連絡先")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                (
                    "child",
                    models.ForeignKey(
                        db_column="children_id",
                        on_delete=models.deletion.CASCADE,
                        related_name="parent_relationships",
                        to="nursery.children",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        db_column="parent_id",
                        on_delete=models.deletion.CASCADE,
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
