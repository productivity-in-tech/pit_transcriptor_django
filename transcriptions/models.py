from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from pathlib import Path
import logging
from urllib.parse import urlsplit, urljoin

from markdown import markdown
import uuid
from .amazon import transcribe

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

    
class Project(models.Model):
    """
    Project Containing Transcriptions
    Project Owners Can View, Edit (without approval), and Delete
    Project Visitors Can View, Request Changes
    """
    name = models.CharField(max_length=255, unique=True, null=False)
    owner = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.SET_NULL)
    url = models.URLField(unique=True)
    can_edit = models.CharField(
            max_length=250,
            default='edit',
            choices=[
                ('edit', 'Edit Without Request'),
                ('request','Request Changes'),
                ('disabled', 'Cannot Edit'),
                ],
            )
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name


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
        if self.status != 'not_started':
            raise ValueError('Project has already been transcribed')

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
        job = transcribe.start_transcription_job(
                TranscriptionJobName=str(self.transcription_key),
                Media={"MediaFileUri": media_file_uri},
                MediaFormat=Path(self.audio_file.name).suffix.lstrip('.'),
                LanguageCode=self.language,
                Settings=_settings,
                )
        self.status = 'in_progress'
        return job


    def __str__(self):
        return self.name


class TranscriptionText(models.Model):
    transcription = models.ForeignKey(Transcription, on_delete=models.CASCADE)
    updated_date = models.DateTimeField(default=timezone.now)
    transcription_text = models.TextField()
    editor = models.ForeignKey(
            UserModel,
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
            )

    def to_markdown(self):
        return markdown(self.transcription_text)

    def __str__(self):
        return self.transcription_text


class BaseSpeaker(models.Model):
    speaker_name = models.CharField(max_length=255)
    speaker_label = models.IntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(10)],
           ) 


class DefaultSpeakers(BaseSpeaker):
    """Default Speakers save a step in defining the speakers in a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


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


class AuthorizedProjectEditor(models.Model):
    """List of authorized editors at the project level. Access at this level
    overrides TranscriptionOnly Listings is used by owners to grant access to
    edit any transcription in a project without the owner having to
    review the changes"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
       return self.user

