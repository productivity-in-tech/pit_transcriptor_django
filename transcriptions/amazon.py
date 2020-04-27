"""
This is the Amazon S3 information from the project.
Any sensitive data is stored in the environment variables and not in this file.
"""
import os
import datetime
import logging

import boto3
import requests

transcribe = boto3.client('transcribe')


def get_transcription(job):
    job_uri = job['TranscriptionJob']["Transcript"]["TranscriptFileUri"]
    r = requests.get(job_uri)
    logging.debug(r.json())
    r.raise_for_status()
    return r.json()


def build_text(transcript_pair, format="MILLER"):
    """Given a speaker ([0]), transcript ([1]) pair. Generate text block with the Speaker,
    Start_time, and Content"""
    speaker, transcript_data = transcript_pair
    # Make the start time into 00:00:00 format
    start_time = str(datetime.timedelta(seconds=round(float(transcript_data['start_time']))))
    content = transcript_data['alternatives'][0]['transcript']
    # Now sew it all together

    if format == "MILLER":
        return f'## {speaker} {start_time}\n\n{content}\n\n'

    if format == "KENNEDY":
        return f'{start_time} {speaker}:\n\n{content}\n\n'


def get_markers(transcript_pairs):
    """equivalent to build text however this does not include the start time"""
    markers = []
    last_speaker = ''

    for speaker, transcript_data in transcript_pairs:
        if speaker != last_speaker:
            markers.append({
                'speaker': speaker,
                'start_time': transcript_data['start_time']})
            last_speaker = speaker

    return markers


def build_speaker_pairs(transcript_json):
    speaker_labels = transcript_json['results']['speaker_labels']['segments']
    speakers = [x['speaker_label'].replace('spk', 'Speaker') for x in speaker_labels]
    return list(zip(speakers, transcript_json['results']['segments']))
