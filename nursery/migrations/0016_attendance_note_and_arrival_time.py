from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0015_attendance_is_confirmed"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendance",
            name="note",
            field=models.TextField(blank=True, default="", verbose_name="特記事項"),
        ),
        migrations.AddField(
            model_name="attendance",
            name="scheduled_arrival_time",
            field=models.TimeField(blank=True, null=True, verbose_name="予定登園時間"),
        ),
    ]
