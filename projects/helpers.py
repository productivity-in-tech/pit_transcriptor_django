from django.core.files import File
from tempfile import TemporaryFile
from pathlib import Path
import requests
import urllib.request
import feedparser
from transcriptions.models import Transcription
from datetime import date
from time import mktime

def get_feed_text(feed_url):
    """retrieves the feed using requests as text to store in the DB and be
    checked against"""

    return requests.get(feed_url).text

def get_feed_item_data(feed_item):
    for link in feed_item['links']:
        if link['type'] == 'text/html':
            url = link['href']

        elif 'audio' in link['type']:
            audio_file = link['href']

    published_parsed = date.fromtimestamp(
            mktime(feed_item['published_parsed']),
            )
    return {
            'title': feed_item['title'],
            'audio_file': audio_file,
            'publish_date': published_parsed,
            'url': url,
            }


def get_feed_data(feed):
    feed_data = feedparser.parse(feed)
    links = []
    for item in feed_data['items']:
        links.append(get_feed_item_data(item))
    return links
    

def transcription_get_or_create(feed_item, project):
    t = Transcription.objects.get_or_create(
            name=feed_item['title'], 
            owner=project.owner,
            transcription_item_publish_date=feed_item['publish_date'],
            project=project,
            defaults = {'status': 'in_progress'}
            )

    if t[1]:
        obj = requests.get(feed_item['audio_file'], stream=True)
        with TemporaryFile() as tempfile:
            tempfile.write(obj.raw.read())
            t[0].audio_file.save(
                    Path(feed_item['audio_file']).name,
                    tempfile,
                    )
        t[0].start_transcription()
        t[0].save()


