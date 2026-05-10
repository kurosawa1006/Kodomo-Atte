from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0017_parent_staff_children_facility_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="parent",
            name="start_date",
            field=models.DateField(blank=True, null=True, verbose_name="開始日"),
        ),
        migrations.AddField(
            model_name="parent",
            name="end_date",
            field=models.DateField(blank=True, null=True, verbose_name="終了日"),
        ),
        migrations.AddField(
            model_name="parent",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="削除フラグ"),
        ),
        migrations.AddField(
            model_name="staff",
            name="start_date",
            field=models.DateField(blank=True, null=True, verbose_name="開始日"),
        ),
        migrations.AddField(
            model_name="staff",
            name="end_date",
            field=models.DateField(blank=True, null=True, verbose_name="終了日"),
        ),
        migrations.AddField(
            model_name="staff",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="削除フラグ"),
        ),
        migrations.AddField(
            model_name="children",
            name="start_date",
            field=models.DateField(blank=True, null=True, verbose_name="開始日"),
        ),
        migrations.AddField(
            model_name="children",
            name="end_date",
            field=models.DateField(blank=True, null=True, verbose_name="終了日"),
        ),
        migrations.AddField(
            model_name="children",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name="削除フラグ"),
        ),
    ]
