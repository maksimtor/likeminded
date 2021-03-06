# Generated by Django 4.0 on 2022-01-17 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_user_room_to_join_user_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchingInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_done', models.BooleanField(default=False, max_length=200)),
                ('room_to_join', models.IntegerField(null=True)),
            ],
        ),
    ]
