import re 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import (
        Transcription,
        )
from projects.models import (
        Project,
        )
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your views here.
def transcription_list(request):
    transcriptions = Transcription.objects.all()

    return render(request, 'transcriptions/transcription_list.html',
            {'transcriptions': transcriptions})

class TranscriptionDetailView(DetailView):
    model = Transcription
    template_name = 'transcriptions/detail.html'

    def get_object(self):
        pk = self.kwargs['pk']
        obj = Transcription.objects.get(pk=pk)
        status = obj.status

        if status.lower() == 'in_progress':
            Transcription.objects.filter(pk=pk).update(
                    status=obj.update_transcription_status().lower())

            obj = Transcription.objects.get(pk=pk)
            if not obj.transcription_text and obj.status == 'complete':
                Transcription.objects.filter(pk=pk).update(
                        transcription_text=obj.build_amazon_speaker_transcription())
                    

        obj = Transcription.objects.get(pk=pk)

        return obj

class TranscriptionTextUpdateView(LoginRequiredMixin, UpdateView):
    model = Transcription
    template_name = 'transcriptions/update-text.html'
    fields = ['transcription_text']

class TranscriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transcription
    template_name = 'transcriptions/update.html'
    fields = [
            'name',
            'audio_file',
            'url',
            'project',
            'language',
            'settings_max_alternatives',
            'settings_max_speaker_labels',
            'transcription_item_publish_date',
            ]

    def get_success_url(self, **kwargs):
        return reverse_lazy('transcription_detail',
                kwargs={'pk': self.object.pk})


class TranscriptionTextUpdateView(LoginRequiredMixin, UpdateView):
    model = Transcription
    fields = ['transcription_text']
    template_name = 'transcriptions/update-text.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.pk},
            )


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Transcription
    template_name = 'transcriptions/create.html'
    fields = [
            'name',
            'audio_file',
            'url',
            'project',
            'language',
            'transcription_item_publish_date',
            ]

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.pk},
            )

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

@require_http_methods(["POST"])
def bulk_replace(request, pk):
    starting_text = Transcription.objects.get(pk=pk).transcription_text
    new_text = re.sub(
            request.POST['search-for'],
            request.POST['replace-with'],
            starting_text,
            re.IGNORECASE,
            )
    Transcription.objects.filter(pk=pk).update(transcription_text=new_text)
    return redirect('transcription_detail', pk=pk)


@require_http_methods(["POST"])
def start_transcription(request, pk):
    Transcription.objects.get(pk=pk).start_transcription()
    Transcription.objects.filter(pk=pk).update(status='in_progress')
    return redirect('transcription_detail', pk=pk)
