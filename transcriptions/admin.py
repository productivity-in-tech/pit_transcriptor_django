from django.contrib import admin
from .models import Transcription, TranscriptionText, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Transcription)
admin.site.register(TranscriptionText)
