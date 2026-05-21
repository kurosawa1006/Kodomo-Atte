import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0007_staff"),
    ]

    operations = [
        migrations.CreateModel(
            name="Children",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="氏名")),
                ("kana", models.CharField(max_length=100, verbose_name="かな")),
                ("birthday", models.DateField(verbose_name="誕生日")),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "男"), ("female", "女"), ("other", "その他")],
                        max_length=10,
                        verbose_name="性別",
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True, verbose_name="開始日")),
                ("end_date", models.DateField(blank=True, null=True, verbose_name="終了日")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "facility",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="nursery.facility",
                        verbose_name="施設ID",
                    ),
                ),
                (
                    "nursery_class",
                    models.ForeignKey(
                        blank=True,
                        db_column="class_id",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="nursery.class",
                        verbose_name="クラス",
                    ),
                ),
                (
                    "sub_class",
                    models.ForeignKey(
                        blank=True,
                        db_column="sub_class_id",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="children",
                        to="nursery.subclass",
                        verbose_name="サブクラス",
                    ),
                ),
            ],
            options={
                "verbose_name": "園児",
                "verbose_name_plural": "園児",
                "ordering": ["nursery_class_id", "kana", "name"],
            },
        ),
    ]
