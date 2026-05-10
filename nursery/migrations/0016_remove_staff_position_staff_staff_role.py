from django.db import migrations, models
import django.db.models.deletion


def forwards_copy_position_to_staff_role(apps, schema_editor):
    Staff = apps.get_model("nursery", "Staff")
    StaffRole = apps.get_model("nursery", "StaffRole")
    for staff in Staff.objects.all():
        if not staff.position:
            continue
        role = StaffRole.objects.filter(name=staff.position).first()
        if role is not None:
            staff.staff_role_id = role.id
            staff.save(update_fields=["staff_role_id"])


class Migration(migrations.Migration):
    dependencies = [
        ("nursery", "0015_staffrole"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="staff_role",
            field=models.ForeignKey(
                blank=True,
                db_column="staffrole_id",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="staff_members",
                to="nursery.staffrole",
                verbose_name="役職",
            ),
        ),
        migrations.RunPython(forwards_copy_position_to_staff_role, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="staff",
            name="position",
        ),
    ]
