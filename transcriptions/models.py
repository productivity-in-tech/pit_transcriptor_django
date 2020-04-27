import re
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from pathlib import Path
import logging
from urllib.parse import urlunsplit, urlsplit, urljoin

import uuid
from . import amazon
from projects.models import Project

# Create your models here.  UserModel = get_user_model()

flags = [
        ('en-US', 'US English'),
        ('en-GB', 'British English'),
        ('es-US', 'US Spanish'),
        ('en-AU', 'Australian English'),
        ('fr-CA', 'Canadian Friend'),
        ('de-DE', 'German'),
        ('pt-BR', 'Brazilian Portuguese'),
        ('fr-FR', 'French'),
        ('it-IT', 'Italian'),
        ('ko-KR', 'Korean'),
        ('es-ES', 'Spanish'),
        ('en-IN', 'Indian English'),
        ('hi-IN', 'Indian Hindi'),
        ('ar-SA', 'Modern Standard Arabic'),
        ('ru-RU', 'Russian'),
        ('zh-CN', 'Mandarin Chinese'),
        ]

UserModel = get_user_model()


class Transcription(models.Model):
    """Individual Transcriptions"""
    audio_file = models.FileField(null=True)
    name = models.CharField(max_length=255, unique=False, null=False)
    transcription_key = models.UUIDField(
            editable=False,
            null=False,
            default=uuid.uuid4,
            )
    url = models.URLField(blank=True, null=True, unique=True)
    settings_show_alternatives = models.BooleanField(default=True)
    settings_max_alternatives = models.IntegerField(
            blank=True,
            validators=[MinValueValidator(2), MaxValueValidator(10)],
            default=2,
           )
    settings_show_speaker_labels = models.BooleanField(default=True)
    settings_max_speaker_labels = models.IntegerField(
            blank=True,
            default=4,
            validators=[MinValueValidator(0), MaxValueValidator(10)],
            )
    transcription_item_publish_date = models.DateField(null=True, blank=True)
    transcription_text = models.TextField(blank=True)
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
            max_length=128,
            default='in_progress',
            )
    created_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=250, default='en-US', choices=flags)
    transcription_format = models.CharField(choices=[
            ('MILLER', 'MILLER Format'),
            ('KENNEDY', 'KENNEDY Format'),
            ],
            max_length=128,
            default='MILLER',
            )

    def start_transcription(self):
        _settings = {
                "ShowAlternatives": self.settings_show_alternatives,
                "MaxAlternatives": self.settings_max_alternatives,
                }

        if getattr(self, 'channel_identification', None):
            _settings.ChannelIdentification = self.channel_identification

        else:
            _settings['ShowSpeakerLabels'] = self.settings_show_speaker_labels
            _settings['MaxSpeakerLabels'] = self.settings_max_speaker_labels

        # Take sheme, netloc, and url from audio_url, to remove any url suffix
        # trash
        media_file_uri = urlunsplit(urlsplit(self.audio_file.url)[:3] + ('', ''))
        job = amazon.transcribe.start_transcription_job(
                TranscriptionJobName=str(self.transcription_key),
                Media={"MediaFileUri": media_file_uri},
                MediaFormat=Path(self.audio_file.name).suffix.lstrip('.'),
                LanguageCode=self.language,
                Settings=_settings,
                )
        return job

    class Meta:
        ordering = ['-transcription_item_publish_date', 'created_date']

    @property
    def job(self):
        return amazon.transcribe.get_transcription_job(
                TranscriptionJobName=str(self.transcription_key)
                )

    def update_transcription_status(self):
        return self.job['TranscriptionJob']['TranscriptionJobStatus'].lower()

    def build_amazon_speaker_transcription(self):
        json_file = amazon.get_transcription(self.job)# returns the Output.json file generated from amazon
        speaker_pairs = amazon.build_speaker_pairs(json_file) # makes speaker/transcript pairs
        transcription_list = list(
                map(
                    lambda x:amazon.build_text(x, self.transcription_format),
                    speaker_pairs)) # the thing that expands the zip files
        transcription_text = ''.join(transcription_list)
        return transcription_text


    def update_transcription_text(self, find_text, replace_text):
        new_text = re.sub(
            find_text,
            replace_text,
            self.transcription_text,
            flags=re.IGNORECASE,
            )
        return new_text

    def __str__(self):
        return self.name


class TranscriptionEdit(models.Model):
    transcription = models.ForeignKey(
                Transcription,
                on_delete=models.CASCADE,
                )
    transcription_text = models.TextField()
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    edited_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
            max_length = 250,
            choices = [
                ('pending_approval', 'Pending Approval'),
                ('overwitten', 'Overwritten'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
                ],
            default = 'pending_approval',
            )

    class Meta:
        ordering = ['-edited_datetime']
        get_latest_by = ['edited_datetime']
