# Generated by Django 3.2 on 2021-05-24 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='actions',
        ),
        migrations.AddField(
            model_name='task',
            name='actions',
            field=models.TextField(blank=True, verbose_name='Действия'),
        ),
    ]
