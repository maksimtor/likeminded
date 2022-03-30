# Generated by Django 4.0 on 2022-04-02 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0024_customuser_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='description',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
