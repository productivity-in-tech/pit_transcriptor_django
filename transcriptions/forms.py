import datetime
from customModelForm import CustomModelForm
from django import forms
from django.db import models
from projects.models import Project

from .models import Transcription

class TranscriptionAddForm(CustomModelForm):
    class Meta:
        model = Transcription
        fields = (
                'name',
                'audio_file',
                'project',
                'url',
                'language',
                'transcription_item_publish_date',
                )
        widgets = {
                'transcription_item_publish_date':
                forms.SelectDateWidget(
                    years = list(
                        range(2000, datetime.datetime.now().year + 1))[::-1],
                    empty_label=(
                        'Select Year', 'Select Month', 'Select Day'),
                    )
                }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'] = forms.ModelChoiceField(
                queryset=Project.objects.filter(owner=request.user),
                required=False,
                )

class TranscriptionUpdateForm(CustomModelForm):
    class Meta:
        model = Transcription
        fields = (
                'name',
                'url',
                'transcription_item_publish_date',
                )

        widgets = {
                'name': forms.TextInput(attrs={'class': 'input'}),
                'url': forms.TextInput(attrs={'class': 'input'}),
                'transcription_item_publish_date':
                forms.SelectDateWidget(
                    years = list(
                        range(2000, datetime.datetime.now().year + 1))[::-1],
                    empty_label=(
                        'Select Year', 'Select Month', 'Select Day'),
                    )
                }
