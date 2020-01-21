# Generated by Django 3.0 on 2020-01-21 19:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_file', models.FileField(null=True, upload_to='')),
                ('name', models.CharField(max_length=255)),
                ('transcription_key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('url', models.URLField(blank=True, null=True, unique=True)),
                ('settings_show_alternatives', models.BooleanField(default=True)),
                ('settings_max_alternatives', models.IntegerField(blank=True, default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(10)])),
                ('settings_show_speaker_labels', models.BooleanField(default=True)),
                ('settings_max_speaker_labels', models.IntegerField(blank=True, default=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('transcription_item_publish_date', models.DateField(blank=True)),
                ('transcription_text', models.TextField(blank=True)),
                ('status', models.CharField(default='in_progress', max_length=128)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(choices=[('en-US', 'US English'), ('en-GB', 'British English'), ('es-US', 'US Spanish'), ('en-AU', 'Australian English'), ('fr-CA', 'Canadian Friend'), ('de-DE', 'German'), ('pt-BR', 'Brazilian Portuguese'), ('fr-FR', 'French'), ('it-IT', 'Italian'), ('ko-KR', 'Korean'), ('es-ES', 'Spanish'), ('en-IN', 'Indian English'), ('hi-IN', 'Indian Hindi'), ('ar-SA', 'Modern Standard Arabic'), ('ru-RU', 'Russian'), ('zh-CN', 'Mandarin Chinese')], default='en-US', max_length=250)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Project')),
            ],
            options={
                'ordering': ['-transcription_item_publish_date', 'created_date'],
            },
        ),
        migrations.CreateModel(
            name='TranscriptionEdit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcription_text', models.TextField()),
                ('edited_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('transcription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transcriptions.Transcription')),
            ],
            options={
                'ordering': ['-edited_datetime'],
                'get_latest_by': ['edited_datetime'],
            },
        ),
    ]
