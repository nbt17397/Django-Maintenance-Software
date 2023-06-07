# Generated by Django 4.1.3 on 2023-06-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0005_rename_project_id_building_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=True),
        ),
    ]