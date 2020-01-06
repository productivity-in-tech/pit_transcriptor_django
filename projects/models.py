from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from pathlib import Path
import logging
from urllib.parse import urlsplit, urljoin

import uuid

# Create your models here.

UserModel = get_user_model()
    
class Project(models.Model):
    """
    Project Containing Transcriptions
    Project Owners Can View, Edit (without approval), and Delete
    Project Visitors Can View, Request Changes
    """
    name = models.CharField(max_length=255, unique=True, null=False)
    owner = models.ForeignKey(
            UserModel,
            blank=True,
            null=True,
            on_delete=models.SET_NULL,
            related_query_name='owner',
            related_name='owner',
            )
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


class BaseSpeaker(models.Model):
    speaker_name = models.CharField(max_length=255)
    speaker_label = models.IntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(10)],
           ) 


class DefaultSpeakers(BaseSpeaker):
    """Default Speakers save a step in defining the speakers in a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class AuthorizedProjectEditor(models.Model):
    """List of authorized editors at the project level. Access at this level
    overrides TranscriptionOnly Listings is used by owners to grant access to
    edit any transcription in a project without the owner having to
    review the changes"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
       return self.user


class ProjectsFollowing(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
