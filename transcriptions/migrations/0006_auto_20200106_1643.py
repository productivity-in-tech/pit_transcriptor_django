# Generated by Django 3.0 on 2020-01-07 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0005_auto_20200106_1637'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcription',
            options={'get_latest_by': ['-created_date', '-transcription_item_publish_date'], 'ordering': ['-created_date', '-transcription_item_publish_date']},
        ),
    ]
