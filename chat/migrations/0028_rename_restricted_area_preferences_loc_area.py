# Generated by Django 4.0 on 2022-04-03 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0027_remove_preferences_loc_area_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferences',
            old_name='restricted_area',
            new_name='loc_area',
        ),
    ]
