# Generated by Django 4.0 on 2023-07-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0034_delete_chat_remove_chatroom_messages_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_1', models.CharField(max_length=200, null=True)),
                ('user_2', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]