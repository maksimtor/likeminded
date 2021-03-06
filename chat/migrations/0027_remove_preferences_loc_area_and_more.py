# Generated by Django 4.0 on 2022-04-03 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0026_historicalchat_customuser_historicalchats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='loc_area',
        ),
        migrations.AddField(
            model_name='preferences',
            name='area_restrict',
            field=models.BooleanField(default=False, max_length=200),
        ),
        migrations.AddField(
            model_name='preferences',
            name='restricted_area',
            field=models.IntegerField(default=10, null=True),
        ),
    ]
