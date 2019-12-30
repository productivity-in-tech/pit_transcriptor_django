import json_builder
import json
import logging
import os
import shutil
import sys
import time
import typing
from pathlib import Path

import click

import boto3
import requests

from dotenv import load_dotenv
load_dotenv()

# Amazon Information
bucket = os.environ.get("BUCKET_NAME", True)
storage = boto3.client("s3")
transcribe = boto3.client("transcribe")
flags = {
    'en-US': 'US English',
    'en-GB': 'British English',
    'es-US': 'US Spanish',
    'en-AU': 'Australian English',
    'fr-CA': 'Canadian Friend',
    'de-DE': 'German',
    'pt-BR': 'Brazilian Portuguese',
    'fr-FR': 'French',
    'it-IT': 'Italian',
    'ko-KR': 'Korean',
    'es-ES': 'Spanish',
    'en-IN': 'Indian English',
    'hi-IN': 'Indian Hindi',
    'ar-SA': 'Modern Standard Arabic',
    'ru-RU': 'Russian',
    'zh-CN': 'Mandarin Chinese',
    }


def start_transcription(
        *,
        job_name,
        key,
        language,
        channel_identification,
        show_speaker_labels,
        max_speaker_labels: int=0,
        storage=storage,
        transcribe=transcribe,
        bucket=bucket,
    ):
    settings={
        "ShowAlternatives": True,
        "MaxAlternatives": 2,
        }

    if channel_identification:
        settings['ChannelIdentification'] = channel_identification

    elif show_speaker_labels and max_speaker_labels > 1:
        settings['ShowSpeakerLabels'] = show_speaker_labels
        settings['MaxSpeakerLabels'] = max_speaker_labels

    transcribe_job_uri = f"https://{bucket}.s3.amazonaws.com/{key}"
    print(transcribe_job_uri)


    return transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": transcribe_job_uri},
        MediaFormat=Path(key).suffix.lstrip('.'),
        LanguageCode=language,
        Settings=settings,
    )


def get_key(file_path):
    return Path(file_path).name.replace(" ", "")


def get_job(key, transcribe=transcribe):
    return transcribe.get_transcription_job(TranscriptionJobName=key)


def check_job_status(job):
    """Calling check skips the transcription starting point
and just checks the status for the file"""
    job_status = job["TranscriptionJob"]["TranscriptionJobStatus"]
    return job_status


def get_transcription(job):
    job_uri = job['TranscriptionJob']["Transcript"]["TranscriptFileUri"]
    r = requests.get(job_uri)
    logging.debug(r.json())
    r.raise_for_status()
    return r.json()


def format_speaker_transcription(job):
    transcript_json = get_transcription(job)
    transcription_data = json_builder.build_speaker_transcript(transcript_json)
    return '\n\n'.join(
            list(map(json_builder.build_text, transcription_data))
            )


if __name__ == "__main__":
    start_transcription()
