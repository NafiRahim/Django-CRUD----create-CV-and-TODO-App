# Generated by Django 5.0.1 on 2024-02-01 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]