from django.contrib import admin
from .models import Transcription, TranscriptionText

# Register your models here.
admin.site.register(Transcription)
admin.site.register(TranscriptionText)
