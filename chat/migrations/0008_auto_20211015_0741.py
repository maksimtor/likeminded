# Generated by Django 3.1.1 on 2021-10-15 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20211009_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extraversion', models.FloatField()),
                ('agreeableness', models.FloatField()),
                ('openness', models.FloatField()),
                ('conscientiousness', models.FloatField()),
                ('neuroticism', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='weights',
        ),
        migrations.AddField(
            model_name='preferences',
            name='loc_area',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='preferences',
            name='personality',
            field=models.CharField(default=False, max_length=200),
        ),
        migrations.DeleteModel(
            name='PrefWeights',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='personality',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.personality'),
        ),
    ]
