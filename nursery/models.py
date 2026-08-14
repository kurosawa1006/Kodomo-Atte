from django.db import models
from django.utils import timezone


class Facility(models.Model):
    name = models.CharField("施設名", max_length=100)
    postal_code = models.CharField("郵便番号", max_length=20, blank=True, default="")
    address = models.CharField("住所", max_length=255)
    phone_number = models.CharField("電話番号", max_length=30)
    capacity = models.PositiveIntegerField("定員")
    is_active = models.BooleanField("有効", default=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "施設"
        verbose_name_plural = "施設"
        ordering = ["name", "id"]

    def __str__(self) -> str:
        return self.name


class Class(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        verbose_name="施設ID",
        related_name="classes",
    )
    name = models.CharField("クラス名", max_length=100)
    description = models.TextField("説明", blank=True, default="")
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "クラス"
        verbose_name_plural = "クラス"
        db_table = "class"
        ordering = ["facility_id", "name", "id"]

    def __str__(self) -> str:
        return self.name


class SubClass(models.Model):
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        verbose_name="施設ID",
        related_name="sub_classes",
    )
    nursery_class = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        verbose_name="クラスID",
        related_name="sub_classes",
        db_column="class_id",
    )
    name = models.CharField("サブクラス名", max_length=100)
    description = models.TextField("説明", blank=True, default="")
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "サブクラス"
        verbose_name_plural = "サブクラス"
        db_table = "sub_class"
        ordering = ["facility_id", "nursery_class_id", "name", "id"]

    def __str__(self) -> str:
        return self.name


class StaffRole(models.Model):
    name = models.CharField("役職名", max_length=100)
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

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
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

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
    last_name = models.CharField("姓", max_length=50)
    first_name = models.CharField("名", max_length=50)
    last_name_kana = models.CharField("姓（かな）", max_length=50)
    first_name_kana = models.CharField("名（かな）", max_length=50)
    phone_number = models.CharField("電話番号", max_length=30)
    postal_code = models.CharField("郵便番号", max_length=20)
    address = models.CharField("住所", max_length=255)
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "スタッフ"
        verbose_name_plural = "スタッフ"
        ordering = ["facility_id", "last_name_kana", "first_name_kana", "last_name", "first_name"]

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def full_kana(self) -> str:
        return f"{self.last_name_kana} {self.first_name_kana}".strip()

    def __str__(self) -> str:
        return f"{self.full_name} ({self.staff_number})"


class Children(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "男"
        FEMALE = "female", "女"
        OTHER = "other", "その他"

    last_name = models.CharField("姓", max_length=50)
    first_name = models.CharField("名", max_length=50)
    last_name_kana = models.CharField("姓（かな）", max_length=50)
    first_name_kana = models.CharField("名（かな）", max_length=50)
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
    nursery_class = models.ForeignKey(
        Class,
        on_delete=models.PROTECT,
        verbose_name="クラス",
        related_name="children",
        db_column="class_id",
        null=True,
        blank=True,
    )
    sub_class = models.ForeignKey(
        SubClass,
        on_delete=models.PROTECT,
        verbose_name="サブクラス",
        related_name="children",
        db_column="sub_class_id",
        null=True,
        blank=True,
    )
    start_date = models.DateField("開始日", null=True, blank=True)
    end_date = models.DateField("終了日", null=True, blank=True)
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "園児"
        verbose_name_plural = "園児"
        ordering = ["nursery_class_id", "last_name_kana", "first_name_kana", "last_name", "first_name"]

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def full_kana(self) -> str:
        return f"{self.last_name_kana} {self.first_name_kana}".strip()

    def __str__(self) -> str:
        class_label = self.nursery_class.name if self.nursery_class_id else "-"
        return f"{self.full_name} ({class_label})"


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
    is_confirmed = models.BooleanField("確認済", default=False)
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "出席"
        verbose_name_plural = "出席"
        constraints = [
            models.UniqueConstraint(fields=["child", "date"], name="uniq_attendance_child_date"),
        ]
        ordering = ["-date", "child__nursery_class_id", "child__last_name_kana", "child__first_name_kana", "child__last_name", "child__first_name"]


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
    is_deleted = models.BooleanField("削除フラグ", default=False)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "保護者-園児リレーション"
        verbose_name_plural = "保護者-園児リレーション"
        db_table = "parent_child_relationships"
        ordering = ["-created_at", "child__last_name_kana", "child__first_name_kana", "parent__kana"]
