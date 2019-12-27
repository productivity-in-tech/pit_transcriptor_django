from django import forms

from .models import Transcription, Project

class TranscriptionAddForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Transcription
        fields = ('name', 'url', 'transcription_item_publish_date', 'project')

class ProjectAddForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'url')
