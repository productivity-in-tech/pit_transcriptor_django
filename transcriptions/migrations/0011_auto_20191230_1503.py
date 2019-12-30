# Generated by Django 3.0 on 2019-12-30 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0010_auto_20191227_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcriptiontext',
            options={'get_latest_by': ['-updated_date']},
        ),
        migrations.AlterField(
            model_name='transcriptiontext',
            name='transcription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TranscribedTexts', to='transcriptions.Transcription'),
        ),
    ]
