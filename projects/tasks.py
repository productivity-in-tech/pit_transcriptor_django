from django.apps import AppConfig
from django.utils import timezone

from .models import Project
from .helpers import transcription_get_or_create 


def check_for_new_files():
    updating_projects = Project.objects.filter(rss_updates=True)

    for project in updating_projects:
        for feed_item in project.feed_data:
            transcription_get_or_create(feed_item, project=project)
