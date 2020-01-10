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
    rss_feed_url = models.URLField(blank=True, null=True)
    rss_updates = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ProjectsFollowing(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
