from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from pathlib import Path
import logging
import feedparser
from urllib.parse import urlparse, urlsplit, urljoin
from datetime import date
from time import mktime

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
    project_image = models.ImageField(null=True, blank=True)
    edit_allowed = models.ManyToManyField(UserModel, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


    @property
    def feed_data(self):
        feed_data_items = []
        parsed_feed = feedparser.parse(self.rss_feed_url)

        for feed_item in parsed_feed['items']:

            for link in feed_item['links']:

                if link['type'] == 'text/html':
                    url = link['href']

                elif 'audio' in link['type']:
                    audio_file = link['href']


            published_parsed = date.fromtimestamp(
                    mktime(feed_item['published_parsed']),
                    )

            feed_data_items.append({
                    'title': feed_item['title'],
                    'audio_file': audio_file,
                    'publish_date': published_parsed,
                    'url': url,
                    })
        return  feed_data_items

    def bulk_replace(self, find_text, replace_text):
        for transcription in Transcription.objects.filter(project=self):
            transcription.update_transcription_text(
                    find_text,
                    replace_text,
                    )

class ProjectDictionaryItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    find_text = models.CharField(max_length=250)
    replace_text = models.CharField(max_length=250)


class ProjectsFollowing(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
