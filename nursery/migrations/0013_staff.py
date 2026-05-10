from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0012_parentchildrelationship_and_remove_parent_relationship"),
    ]

    operations = [
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("facility_id", models.CharField(max_length=50, verbose_name="施設ID")),
                ("staff_number", models.CharField(max_length=50, verbose_name="スタッフナンバー")),
                ("position", models.CharField(max_length=100, verbose_name="役職")),
                ("name", models.CharField(max_length=100, verbose_name="氏名")),
                ("kana", models.CharField(max_length=100, verbose_name="かな")),
                ("phone_number", models.CharField(max_length=30, verbose_name="電話番号")),
                ("postal_code", models.CharField(max_length=20, verbose_name="郵便番号")),
                ("address", models.CharField(max_length=255, verbose_name="住所")),
            ],
            options={
                "verbose_name": "スタッフ",
                "verbose_name_plural": "スタッフ",
                "ordering": ["facility_id", "kana", "name", "id"],
            },
        ),
    ]
