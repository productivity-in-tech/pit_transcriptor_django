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
        TranscriptionText,
        )
from projects.models import (
        Project,
        ProjectsFollowing,
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
        obj = Transcription.objects.filter(pk=pk).first()
        status = obj.status
        print(obj.latest_transcription == None)

        if status.lower() not in ['completed', 'not_started']:
            new_status = obj.update_transcription_status()
            Transcription.objects.filter(pk=pk).update(status=new_status)


        if obj.latest_transcription == None and obj.status == 'completed':
            transcription_text = obj.build_amazon_speaker_transcription()
            TranscriptionText.objects.get_or_create(
                transcription = obj,
                transcription_text=transcription_text,
                )

        obj = Transcription.objects.get(pk=pk)

        return obj


class TranscriptionUpdateView(UpdateView):
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
                kwargs={'pk':self.object.pk})


class TranscriptionTextCreateView(LoginRequiredMixin, CreateView):
    model = TranscriptionText
    fields = ['transcription_text']

    def form_valid(self, form):
        form.instance.editor = self.request.user
        self.instance.transcription = self.request.transcription

        if form.instance.transcription.owner == self.request.user:
            form.instance.status = 'approved' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transcription_pk = self.kwargs['transcription_pk']
        context['transcription'] = Transcription.objects.get(pk=transcription_pk)
        return context



class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = TranscriptionText
    template_name = 'transcriptions/create.html'
    fields = [
            'name',
            'audio_file',
            'url',
            'project',
            'language',
            'transcription_item_publish_date',
            ]
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@require_http_methods(["POST"])
def start_transcription(request, pk):
    Transcription.objects.get(pk=pk).start_transcription()
    Transcription.objects.filter(pk=pk).update(status='in_progress')
    return redirect('transcription_detail', pk=pk)


