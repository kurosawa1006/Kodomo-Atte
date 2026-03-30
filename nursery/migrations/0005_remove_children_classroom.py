from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nursery", "0004_children_facility_class_ids"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="children",
            name="classroom",
        ),
    ]

