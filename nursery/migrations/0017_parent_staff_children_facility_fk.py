import django.db.models.deletion
from django.db import migrations, models


def forwards_migrate_facility_fk(apps, schema_editor):
    Facility = apps.get_model("nursery", "Facility")
    Parent = apps.get_model("nursery", "Parent")
    Staff = apps.get_model("nursery", "Staff")
    Children = apps.get_model("nursery", "Children")

    valid_ids = {str(pk) for pk in Facility.objects.values_list("id", flat=True)}

    for model in (Parent, Staff, Children):
        for obj in model.objects.all():
            legacy = (getattr(obj, "facility_legacy_id", None) or "").strip()
            if legacy in valid_ids:
                obj.facility_id = int(legacy)
                obj.save(update_fields=["facility_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0016_remove_staff_position_staff_staff_role"),
    ]

    operations = [
        migrations.RenameField(
            model_name="parent",
            old_name="facility_id",
            new_name="facility_legacy_id",
        ),
        migrations.RenameField(
            model_name="staff",
            old_name="facility_id",
            new_name="facility_legacy_id",
        ),
        migrations.RenameField(
            model_name="children",
            old_name="facility_id",
            new_name="facility_legacy_id",
        ),
        migrations.AddField(
            model_name="parent",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="parents",
                to="nursery.facility",
                verbose_name="施設ID",
            ),
        ),
        migrations.AddField(
            model_name="staff",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="staff",
                to="nursery.facility",
                verbose_name="施設ID",
            ),
        ),
        migrations.AddField(
            model_name="children",
            name="facility",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="children",
                to="nursery.facility",
                verbose_name="施設ID",
            ),
        ),
        migrations.RunPython(forwards_migrate_facility_fk, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="parent",
            name="facility_legacy_id",
        ),
        migrations.RemoveField(
            model_name="staff",
            name="facility_legacy_id",
        ),
        migrations.RemoveField(
            model_name="children",
            name="facility_legacy_id",
        ),
    ]
