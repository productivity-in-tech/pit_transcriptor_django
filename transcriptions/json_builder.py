from jinja2 import Markup
from markdown import markdown
import datetime
import json
import logging
import re
import sys

def build_text(transcript_pair):
    """Given a speaker ([0]), transcript ([1]) pair. Generate text block with the Speaker,
    Start_time, and Content"""
    speaker, transcript_data = transcript_pair
    # Make the start time into 00:00:00 format
    start_time = str(datetime.timedelta(seconds=round(float(transcript_data['start_time']))))
    content = transcript_data['alternatives'][0]['transcript']
    # Now sew it all together
    return f"""{speaker} {start_time}
{content}"""

def build_speaker_transcript(transcript_json):
    speaker_labels = transcript_json['results']['speaker_labels']['segments']
    speakers = [x['speaker_label'].replace('spk', 'Speaker') for x in speaker_labels]
    return list(zip(speakers, transcript_json['results']['segments']))
