# Generated by Django 4.1.3 on 2023-08-01 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0006_remove_maintenancedevice_is_part_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='maintenancetask',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='maintenancetask',
            name='maintenance_device_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_task_ids', to='maintenance.maintenancedeviceitem'),
        ),
        migrations.AlterUniqueTogether(
            name='maintenancetask',
            unique_together={('name', 'maintenance_device_item')},
        ),
        migrations.RemoveField(
            model_name='maintenancetask',
            name='maintenance_device',
        ),
    ]
