# Generated by Django 4.1.3 on 2023-06-05 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0004_alter_maintenancetaskdocument_maintenance_task_document_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='buildingdetail',
            old_name='building_id',
            new_name='building',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='process_id',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='device',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='devicedocument',
            old_name='process_id',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='maintenancearea',
            old_name='building_detail_id',
            new_name='building_detail',
        ),
        migrations.RenameField(
            model_name='maintenanceareadetail',
            old_name='maintenance_area_id',
            new_name='maintenance_area',
        ),
        migrations.RenameField(
            model_name='maintenancedevice',
            old_name='device_id',
            new_name='device',
        ),
        migrations.RenameField(
            model_name='maintenancedevice',
            old_name='maintenance_area_detail_id',
            new_name='maintenance_area_detail',
        ),
        migrations.RenameField(
            model_name='maintenancedevice',
            old_name='section_id',
            new_name='section',
        ),
        migrations.RenameField(
            model_name='maintenancetask',
            old_name='checking_way_id',
            new_name='checking_way',
        ),
        migrations.RenameField(
            model_name='maintenancetask',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='maintenancetask',
            old_name='maintenance_device_id',
            new_name='maintenance_device',
        ),
        migrations.RenameField(
            model_name='maintenancetask',
            old_name='step_id',
            new_name='step',
        ),
        migrations.RenameField(
            model_name='maintenancetaskdocument',
            old_name='maintenance_task_document_id',
            new_name='maintenance_task_document',
        ),
        migrations.RenameField(
            model_name='processsection',
            old_name='process_id',
            new_name='process',
        ),
        migrations.RenameField(
            model_name='processstep',
            old_name='checking_way_id',
            new_name='checking_way',
        ),
        migrations.RenameField(
            model_name='processstep',
            old_name='section_id',
            new_name='section',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='manager_id',
            new_name='manager',
        ),
        migrations.AlterField(
            model_name='devicedocument',
            name='path',
            field=models.FileField(null=True, upload_to='device_document/path/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='maintenancetaskdocument',
            name='path',
            field=models.FileField(null=True, upload_to='maintenance_task_document/path/%Y/%m'),
        ),
    ]