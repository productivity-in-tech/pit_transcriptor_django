from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from pathlib import Path
import logging
from urllib.parse import urlsplit, urljoin

import uuid
from . import amazon
from projects.models import Project

# Create your models here.
UserModel = get_user_model()

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

    
class Transcription(models.Model):
    """Individual Transcriptions"""
    audio_file = models.FileField(null=True)
    name = models.CharField(max_length=255, unique=False, null=False)
    transcription_key = models.UUIDField(
            editable=False,
            null=False,
            default=uuid.uuid4,
            )
    url = models.URLField()
    settings_show_alternatives = models.BooleanField(default=True)
    settings_max_alternatives = models.IntegerField(
            blank=True,
            validators=[MinValueValidator(2), MaxValueValidator(10)],
            default=2,
           )
    settings_show_speaker_labels = models.BooleanField(default=True)
    settings_max_speaker_labels = models.IntegerField(
            blank=True,
            default=2,
            validators=[MinValueValidator(0), MaxValueValidator(10)],
            )
    transcription_item_publish_date = models.DateField(blank=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
            max_length=128,
            choices=[('not_started', 'NOT STARTED'), ('in_progress', 'IN PROGRESS'), ('failed', 'ERROR'),
                ('success', 'COMPLETED'), ('pending', 'PENDING_CHANGE')],
            default='not_started',
            )
    created_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=250, default='en-US', choices=flags)

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

        media_file_uri = urlsplit(self.audio_file.url,
            allow_fragments=False)._replace(query=None).geturl()
        logging.warning(f'{media_file_uri=}')
        job = amazon.transcribe.start_transcription_job(
                TranscriptionJobName=str(self.transcription_key),
                Media={"MediaFileUri": media_file_uri},
                MediaFormat=Path(self.audio_file.name).suffix.lstrip('.'),
                LanguageCode=self.language,
                Settings=_settings,
                )
        return job

    @property
    def job(self):
        return amazon.transcribe.get_transcription_job(
                TranscriptionJobName=str(self.transcription_key)
                )

    def update_transcription_status(self):
        status = self.job['TranscriptionJob']['TranscriptionJobStatus'].lower()
        return status

    def build_amazon_speaker_transcription(self):
        json_file = amazon.get_transcription(self.job)# returns the Output.json file generated from amazon
        speaker_pairs = amazon.build_speaker_pairs(json_file) # makes speaker/transcript pairs
        transcription_list = list(map(amazon.build_text, speaker_pairs)) # the thing that expands the zip files
        transcription_text = '\n\n\n'.join(transcription_list)
        print(transcription_text)
        return transcription_text

    @property
    def latest_transcription(self):

        try:
            return self.TranscribedTexts.latest().transcription_text

        except:
            pass


    def __str__(self):
        return self.name


class TranscriptionText(models.Model):
    transcription = models.ForeignKey(
            Transcription,
            on_delete=models.CASCADE,
            related_name='TranscribedTexts',
            )
    updated_date = models.DateTimeField(default=timezone.now)
    transcription_text = models.TextField()
    editor = models.ForeignKey(
            UserModel,
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
            )


    class Meta:
        get_latest_by = ['-updated_date']

    def __str__(self):
        return self.transcription_text


class BaseSpeaker(models.Model):
    speaker_name = models.CharField(max_length=255)
    speaker_label = models.IntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(10)],
           ) 


class TranscriptionSpeaker(BaseSpeaker):
    transcription = models.ForeignKey(Transcription, on_delete=models.CASCADE)


class AuthorizedTranscriptionEditor(models.Model):
    """List of authorized editors at the project or transcription level. This
    is used by owners to grant access to edit a transcription without the owner having to
    review the changes"""

    transcription = models.ForeignKey(Transcription, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
       return self.user
