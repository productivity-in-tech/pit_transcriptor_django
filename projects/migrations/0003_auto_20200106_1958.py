# Generated by Django 3.0 on 2020-01-07 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200106_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaultspeakers',
            name='basespeaker_ptr',
        ),
        migrations.RemoveField(
            model_name='defaultspeakers',
            name='project',
        ),
        migrations.DeleteModel(
            name='BaseSpeaker',
        ),
        migrations.DeleteModel(
            name='DefaultSpeakers',
        ),
    ]
