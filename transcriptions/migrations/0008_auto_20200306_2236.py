# Generated by Django 3.0 on 2020-03-07 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcriptions', '0007_transcription_transcription_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transcription',
            name='transcription_format',
            field=models.CharField(choices=[('MILLER', 'MILLER Format'), ('KENNEDY', 'KENNEDY Format')], default='MILLER', max_length=128),
        ),
    ]
