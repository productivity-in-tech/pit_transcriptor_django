from django.core.files import File
from tempfile import TemporaryFile
from pathlib import Path
import requests
import feedparser
from transcriptions.models import Transcription
from datetime import date
from time import mktime
from urllib.parse import urlsplit, urlunsplit

def transcription_get_or_create(feed_item, project):
    t = Transcription.objects.get_or_create(
            name=feed_item['title'], 
            owner=project.owner,
            transcription_item_publish_date=feed_item['publish_date'],
            project=project,
            defaults = {'status': 'not_started'}
            )

    if t[1]:
        obj = requests.get(feed_item['audio_file'], stream=True)
        with TemporaryFile() as tempfile:
            tempfile.write(obj.raw.read())
            audio_file = urlunsplit(
                    urlsplit(feed_item['audio_file'])[:3] + ('',''))
            t[0].audio_file.save(
                    Path(audio_file).name,
                    tempfile,
                    )

