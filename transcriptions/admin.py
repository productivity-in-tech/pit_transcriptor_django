from django.contrib import admin
from .models import Transcription, TranscriptionEdit

# Register your models here.
admin.site.register(Transcription)
admin.site.register(TranscriptionEdit)
