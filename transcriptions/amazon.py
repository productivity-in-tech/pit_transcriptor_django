"""
This is the Amazon S3 information from the project.
Any sensitive data is stored in the environment variables and not in this file.
"""
import os

import boto3

transcribe = boto3.client('transcribe')


def check_transcription(key):
    return 'Test'


def get_transcription(job):
    job_uri = job['TranscriptionJob']["Transcript"]["TranscriptFileUri"]
    r = requests.get(job_uri)
    logging.debug(r.json())
    r.raise_for_status()
    return r.json()


def build_text(transcript_pair):
    """Given a speaker ([0]), transcript ([1]) pair. Generate text block with the Speaker,
    Start_time, and Content"""
    speaker, transcript_data = transcript_pair
    # Make the start time into 00:00:00 format
    start_time = str(datetime.timedelta(seconds=round(float(transcript_data['start_time']))))
    content = transcript_data['alternatives'][0]['transcript']
    # Now sew it all together
    return f'{speaker} {start_time}\n{content}'

def build_speaker_transcript(transcript_json):
    speaker_labels = transcript_json['results']['speaker_labels']['segments']
    speakers = [x['speaker_label'].replace('spk', 'Speaker') for x in speaker_labels]
    return list(zip(speakers, transcript_json['results']['segments']))


def format_speaker_transcription(job):
    transcript_json = get_transcription(job)
    transcription_data = build_speaker_transcript(transcript_json)
    return '\n\n'.join(
            list(map(build_text, transcription_data))
            )

