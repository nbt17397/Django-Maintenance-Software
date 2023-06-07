# Generated by Django 4.1.3 on 2023-06-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0008_alter_project_ending_date_alter_project_manager_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(0, 'stock'), (1, 'ready'), (2, 'running'), (3, 'replaced'), (4, 'removed')], default=0),
        ),
    ]