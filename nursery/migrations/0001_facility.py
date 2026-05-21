from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Facility",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="施設名")),
                ("postal_code", models.CharField(blank=True, default="", max_length=20, verbose_name="郵便番号")),
                ("address", models.CharField(max_length=255, verbose_name="住所")),
                ("phone_number", models.CharField(max_length=30, verbose_name="電話番号")),
                ("capacity", models.PositiveIntegerField(verbose_name="定員")),
                ("is_active", models.BooleanField(default=True, verbose_name="有効")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
            ],
            options={
                "verbose_name": "施設",
                "verbose_name_plural": "施設",
                "ordering": ["name", "id"],
            },
        ),
    ]
