from django import forms

from .models import Transcription, TranscriptionText

class TranscriptionAddForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Transcription
        fields = ('name', 'url', 'transcription_item_publish_date', 'project')


class TranscriptionTextAddFOrm(forms.ModelForm):
    
    class Meta:
        model = TranscriptionText
        fields = ('transcription_text')
