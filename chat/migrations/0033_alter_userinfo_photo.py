# Generated by Django 4.0 on 2022-04-13 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0032_alter_userinfo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='photo',
            field=models.ImageField(null=True, upload_to='photos'),
        ),
    ]
