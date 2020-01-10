from django_q.models import Schedule
from django.utils import timezone

from .models import Project
from .helpers import transcription_get_or_create 


def check_for_new_files():
    updating_projects = Project.objects.filter(rss_updates=True)

    for project in projects:
        feed_data =  get_feed_data()

        for item in feed_data:
            transcription_get_or_create(feed_item, project=project)
            
