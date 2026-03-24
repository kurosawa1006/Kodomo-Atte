from django.db import models


class Children(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        OTHER = "other", "その他"

    name = models.CharField("氏名", max_length=100)
    kana = models.CharField("かな", max_length=100)
    birthday = models.DateField("誕生日")
    gender = models.CharField("性別", max_length=10, choices=Gender.choices)
    classroom = models.CharField("クラス", max_length=50)

    class Meta:
        verbose_name = "園児"
        verbose_name_plural = "園児"
        ordering = ["classroom", "kana", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.classroom})"
