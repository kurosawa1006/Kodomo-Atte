from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0014_facility_postal_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="役職名")),
            ],
            options={
                "verbose_name": "スタッフロール",
                "verbose_name_plural": "スタッフロール",
                "ordering": ["name", "id"],
            },
        ),
    ]
