from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0003_subclass"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="役職名")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
            ],
            options={
                "verbose_name": "スタッフロール",
                "verbose_name_plural": "スタッフロール",
                "ordering": ["name", "id"],
            },
        ),
    ]
