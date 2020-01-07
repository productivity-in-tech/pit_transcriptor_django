from django import forms
from django.db import models
from projects.models import Project

from .models import Transcription

class TranscriptionAddForm(forms.ModelForm):
    class Meta:
        model = Transcription
        fields = ('name', 'url', 'transcription_item_publish_date', 'project')
        widgets = {
                'project':forms.ModelChoiceField(
                    queryset=Project.objects.filter(user=self.request.user),
                    empty_label="Unnassigned",
                    ),
                }

