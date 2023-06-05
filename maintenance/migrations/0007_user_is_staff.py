# Generated by Django 4.1.3 on 2023-06-05 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0006_remove_user_first_name_remove_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
