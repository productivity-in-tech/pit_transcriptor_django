from django.test import TestCase
from .models import Transcription


class TranscriptionTestCase(TestCase):
    def setUp(self):
        Transcription.objects.create(
                name='test object 1',
                audio_file = None,
                )


