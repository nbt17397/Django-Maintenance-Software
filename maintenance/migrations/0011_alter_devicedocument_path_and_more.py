# Generated by Django 4.1.3 on 2023-06-06 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0010_alter_maintenancetask_ending_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicedocument',
            name='path',
            field=models.FileField(null=True, upload_to='device-document/path/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='maintenancetaskdocument',
            name='path',
            field=models.FileField(null=True, upload_to='maintenance-task-document/path/%Y/%m'),
        ),
    ]