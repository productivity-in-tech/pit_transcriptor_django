# Generated by Django 3.0 on 2020-01-16 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0016_transcriptionedit_transcription_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcriptionedit',
            options={'get_latest_by': ['edited_datetime'], 'ordering': ['-edited_datetime']},
        ),
        migrations.AlterField(
            model_name='transcription',
            name='status',
            field=models.CharField(default='in_progress', max_length=128),
        ),
    ]
