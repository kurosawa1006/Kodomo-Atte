import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0006_parent"),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("staff_number", models.CharField(max_length=50, verbose_name="スタッフナンバー")),
                ("name", models.CharField(max_length=100, verbose_name="氏名")),
                ("kana", models.CharField(max_length=100, verbose_name="かな")),
                ("phone_number", models.CharField(max_length=30, verbose_name="電話番号")),
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
                        related_name="staff",
                        to="nursery.facility",
                        verbose_name="施設ID",
                    ),
                ),
                (
                    "staff_role",
                    models.ForeignKey(
                        blank=True,
                        db_column="staffrole_id",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="staff_members",
                        to="nursery.staffrole",
                        verbose_name="役職",
                    ),
                ),
            ],
            options={
                "verbose_name": "スタッフ",
                "verbose_name_plural": "スタッフ",
                "ordering": ["facility_id", "kana", "name", "id"],
            },
        ),
    ]
