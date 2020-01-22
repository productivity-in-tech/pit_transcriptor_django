import re 

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect

# Local Modules
from .models import (
        Transcription,
        TranscriptionEdit,
        )
from .forms import TranscriptionAddForm, TranscriptionUpdateForm
from premium_check import is_premium

# Project App Modules
from projects.models import (
        Project,
        )

# Create your views here.
class UserTranscriptionListView(LoginRequiredMixin, ListView):
    model = Transcription
    template_name = 'list.html'

    def get_queryset(self):
        return Transcription.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = is_premium(self.request.user)
        return context


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Transcription
    template_name = 'transcriptions/create.html'
    form = TranscriptionAddForm

    def get_form(self, **kwargs):
        form = super().get_form(**kwargs)
        form.fields['project'].queryset(
                Project.objects.filter(owner=self.request.user),
                )

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.pk},
            )

    def form_invalid(self, form):
            print(f'{form.non_field_errors=}')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TranscriptionDeleteView(DeleteView):
    model = Transcription
    template_name = 'delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'project_detail',
            kwargs={'pk': self.object.project.pk},
            )


class TranscriptionDetailView(DetailView):
    """The Main Transcription Detail Information"""
    model = Transcription
    template_name = 'transcriptions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = is_premium(self.request.user)
        return context

    def get_object(self):
        pk = self.kwargs['pk']
        obj = Transcription.objects.get(pk=pk)
        status = obj.status

        if status.lower() == 'in_progress':
            print(status)
            Transcription.objects.filter(pk=pk).update(
                    status=obj.update_transcription_status().lower())

            obj = Transcription.objects.get(pk=pk)
            if not obj.transcription_text and obj.status == 'completed':
                Transcription.objects.filter(pk=pk).update(
                        transcription_text=obj.build_amazon_speaker_transcription())
                    

        obj = Transcription.objects.get(pk=pk)

        return obj

class TranscriptionUpdateView(LoginRequiredMixin, UpdateView):
    """Edit the transcription settings. This DOES NOT allow for updating the
    transcription_text"""
    model = Transcription
    template_name = 'transcriptions/update.html'
    form_class = TranscriptionUpdateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('transcription_detail',
                kwargs={'pk': self.object.pk})


class TranscriptionTextCreateView(LoginRequiredMixin, CreateView):
    """Create a version of the transcription text with Edits"""
    model = TranscriptionEdit
    fields = ['transcription_text']
    template_name = 'transcriptions/update-text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transcription'] = Transcription.objects.get(
                pk = self.kwargs.get('transcription_pk')
                )
        context['subscription'] = is_premium(self.request.user)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['transcription_text'] = Transcription.objects.get(
                pk = self.kwargs.get('transcription_pk'),
                ).transcription_text
        return initial



    def form_valid(self, form):
        form['user'] = self.request.user
        form['transcription'] = self.kwargs.get('transcription_pk')
        return super().form_valid()

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.pk},
            )


class TranscriptionTextModeratedUpdateView(LoginRequiredMixin, UpdateView):
    model = Transcription
    template_name = 'update-text.html'
    fields = ['transcription_text']

    def get_queryset(self):
        return TranscriptionEdit.objects.filter(
                transcription=self.kwargs.get('pk'),
                )

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.project.pk},
            )

class TranscriptionTextModeratedApprovalView(LoginRequiredMixin, UpdateView):
    pass

@require_http_methods(["POST"])
def bulk_replace(request, pk):
    return Transcription.objects.get(pk=pk).update_transcription_text(
            find_text=request.POST['search-for'],
            replace_text=request.POST['replace-with'],
            )
    return redirect('transcription_detail', pk=pk)


@require_http_methods(["POST"])
def start_transcription(request, pk):
    Transcription.objects.get(pk=pk).start_transcription()
    Transcription.objects.filter(pk=pk).update(status='in_progress')
    return redirect('transcription_detail', pk=pk)


def download_transcription_text(request, pk):
    transcription = Transcription.objects.get(pk=pk)
    content = transcription.transcription_text
    content_disposition = f'attachment; filename={transcription.name}.txt'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = content_disposition
    return response


