# Generated by Django 3.0 on 2020-01-07 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200106_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='can_edit',
        ),
    ]