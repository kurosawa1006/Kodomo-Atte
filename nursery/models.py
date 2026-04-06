from django.db import models
from django.utils import timezone


class Children(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        OTHER = "other", "その他"

    name = models.CharField("氏名", max_length=100)
    kana = models.CharField("かな", max_length=100)
    birthday = models.DateField("誕生日")
    gender = models.CharField("性別", max_length=10, choices=Gender.choices)
    facility_id = models.CharField("施設ID", max_length=50, default="1")
    class_id = models.CharField("クラスID", max_length=50, default="1")
    sub_class_id = models.CharField("サブクラスID", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "園児"
        verbose_name_plural = "園児"
        ordering = ["class_id", "kana", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.class_id})"


class Attendance(models.Model):
    child = models.ForeignKey(Children, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField("日付", default=timezone.now)
    class AttendanceStatus(models.IntegerChoices):
        LATE = 1, "遅刻"
        EARLY_LEAVE = 2, "早退"
        ABSENT = 3, "欠席"

    # null は「出席（通常）」を表す
    attendance_status = models.IntegerField(
        "出欠状況",
        choices=AttendanceStatus.choices,
        null=True,
        blank=True,
    )
    reason = models.CharField("欠席理由", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "出席"
        verbose_name_plural = "出席"
        constraints = [
            models.UniqueConstraint(fields=["child", "date"], name="uniq_attendance_child_date"),
        ]
        ordering = ["-date", "child__class_id", "child__kana", "child__name"]
