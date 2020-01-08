from rest_framework import serializers
from .models import Transcription

class TranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
