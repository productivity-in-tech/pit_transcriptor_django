# Generated by Django 3.0 on 2020-01-14 01:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transcriptions', '0013_auto_20200110_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranscriptionEdit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edited_datetime', models.DateTimeField(default=datetime.datetime(2020, 1, 14, 1, 43, 6, 414395, tzinfo=utc))),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('transcription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transcriptions.Transcription')),
            ],
            options={
                'ordering': ['-edited_datetime'],
            },
        ),
    ]
