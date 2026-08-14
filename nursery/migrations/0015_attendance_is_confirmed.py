from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0014_staff_split_kana"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="is_confirmed",
            field=models.BooleanField(default=False, verbose_name="確認済"),
        ),
    ]
