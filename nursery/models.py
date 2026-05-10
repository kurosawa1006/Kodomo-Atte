from django.db import models
from django.utils import timezone


class Facility(models.Model):
    name = models.CharField("施設名", max_length=100)
    postal_code = models.CharField("郵便番号", max_length=20, blank=True, default="")
    address = models.CharField("住所", max_length=255)
    phone_number = models.CharField("電話番号", max_length=30)
    capacity = models.PositiveIntegerField("定員")
    is_active = models.BooleanField("有効", default=True)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "施設"
        verbose_name_plural = "施設"
        ordering = ["name", "id"]

    def __str__(self) -> str:
        return self.name


class StaffRole(models.Model):
    name = models.CharField("役職名", max_length=100)

    class Meta:
        verbose_name = "スタッフロール"
        verbose_name_plural = "スタッフロール"
        ordering = ["name", "id"]

    def __str__(self) -> str:
        return self.name


class Parent(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        verbose_name="施設ID",
        related_name="parents",
        null=True,
        blank=True,
    )
    name = models.CharField("氏名", max_length=100)
    kana = models.CharField("かな", max_length=100)
    phone_number = models.CharField("電話番号", max_length=30)
    emergency_contact = models.CharField("緊急連絡先", max_length=30)
    postal_code = models.CharField("郵便番号", max_length=20)
    address = models.CharField("住所", max_length=255)
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)

    class Meta:
        verbose_name = "保護者"
        verbose_name_plural = "保護者"
        ordering = ["facility_id", "kana", "name", "id"]

    def __str__(self) -> str:
        return self.name


class Staff(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        verbose_name="施設ID",
        related_name="staff",
        null=True,
        blank=True,
    )
    staff_number = models.CharField("スタッフナンバー", max_length=50)
    staff_role = models.ForeignKey(
        StaffRole,
        on_delete=models.PROTECT,
        related_name="staff_members",
        db_column="staffrole_id",
        verbose_name="役職",
        null=True,
        blank=True,
    )
    name = models.CharField("氏名", max_length=100)
    kana = models.CharField("かな", max_length=100)
    phone_number = models.CharField("電話番号", max_length=30)
    postal_code = models.CharField("郵便番号", max_length=20)
    address = models.CharField("住所", max_length=255)
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)

    class Meta:
        verbose_name = "スタッフ"
        verbose_name_plural = "スタッフ"
        ordering = ["facility_id", "kana", "name", "id"]

    def __str__(self) -> str:
        return f"{self.name} ({self.staff_number})"


class Children(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        OTHER = "other", "その他"

    name = models.CharField("氏名", max_length=100)
    kana = models.CharField("かな", max_length=100)
    birthday = models.DateField("誕生日")
    gender = models.CharField("性別", max_length=10, choices=Gender.choices)
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        verbose_name="施設ID",
        related_name="children",
        null=True,
        blank=True,
    )
    class_id = models.CharField("クラスID", max_length=50, default="1")
    sub_class_id = models.CharField("サブクラスID", max_length=50, null=True, blank=True)
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)

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


class ParentChildRelationship(models.Model):
    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="child_relationships",
        db_column="parent_id",
    )
    child = models.ForeignKey(
        Children,
        on_delete=models.CASCADE,
        related_name="parent_relationships",
        db_column="children_id",
    )
    relationship_type = models.CharField("続柄", max_length=50)
    is_main_contact = models.BooleanField("主連絡先", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    class Meta:
        verbose_name = "保護者-園児リレーション"
        verbose_name_plural = "保護者-園児リレーション"
        db_table = "parent_child_relationships"
        ordering = ["-created_at", "child__kana", "parent__kana"]
