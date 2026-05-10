from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0010_facility"),
    ]

    operations = [
        migrations.CreateModel(
            name="Parent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("facility_id", models.CharField(max_length=50, verbose_name="施設ID")),
                ("name", models.CharField(max_length=100, verbose_name="氏名")),
                ("kana", models.CharField(max_length=100, verbose_name="かな")),
                ("phone_number", models.CharField(max_length=30, verbose_name="電話番号")),
                ("emergency_contact", models.CharField(max_length=30, verbose_name="緊急連絡先")),
                ("relationship", models.CharField(max_length=50, verbose_name="続柄")),
                ("postal_code", models.CharField(max_length=20, verbose_name="郵便番号")),
                ("address", models.CharField(max_length=255, verbose_name="住所")),
            ],
            options={
                "verbose_name": "保護者",
                "verbose_name_plural": "保護者",
                "ordering": ["facility_id", "kana", "name", "id"],
            },
        ),
    ]
