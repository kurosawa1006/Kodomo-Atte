from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0013_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="postal_code",
            field=models.CharField(blank=True, default="", max_length=20, verbose_name="郵便番号"),
        ),
    ]
