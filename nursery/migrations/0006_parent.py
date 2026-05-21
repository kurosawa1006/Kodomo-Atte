import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0005_load_staff_roles"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="氏名")),
                ("kana", models.CharField(max_length=100, verbose_name="かな")),
                ("phone_number", models.CharField(max_length=30, verbose_name="電話番号")),
                ("emergency_contact", models.CharField(max_length=30, verbose_name="緊急連絡先")),
                ("postal_code", models.CharField(max_length=20, verbose_name="郵便番号")),
                ("address", models.CharField(max_length=255, verbose_name="住所")),
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
                        related_name="parents",
                        to="nursery.facility",
                        verbose_name="施設ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "保護者",
                "verbose_name_plural": "保護者",
                "ordering": ["facility_id", "kana", "name", "id"],
            },
        ),
    ]
