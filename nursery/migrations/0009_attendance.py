import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0008_children"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(default=django.utils.timezone.now, verbose_name="日付")),
                (
                    "attendance_status",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "遅刻"), (2, "早退"), (3, "欠席")],
                        null=True,
                        verbose_name="出欠状況",
                    ),
                ),
                ("reason", models.CharField(blank=True, default="", max_length=255, verbose_name="欠席理由")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="削除フラグ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="作成日時")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendances",
                        to="nursery.children",
                    ),
                ),
            ],
            options={
                "verbose_name": "出席",
                "verbose_name_plural": "出席",
                "ordering": ["-date", "child__nursery_class_id", "child__kana", "child__name"],
            },
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(fields=("child", "date"), name="uniq_attendance_child_date"),
        ),
    ]
