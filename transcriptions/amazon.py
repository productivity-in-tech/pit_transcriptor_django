"""
This is the Amazon S3 information from the project.
Any sensitive data is stored in the environment variables and not in this file.
"""
import os

import boto3

transcribe = boto3.client('transcribe')


def check_transcription(key):
    return 'Test'

