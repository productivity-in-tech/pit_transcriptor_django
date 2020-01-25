import re

from django import forms
import datetime
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    """View a list of all the Transcriptions Created by the LoggedInUser"""
    model = Transcription
    template_name = 'list.html'

    def get_queryset(self):
        return Transcription.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = is_premium(self.request.user)
        return context


class TranscriptionCreateView(LoginRequiredMixin, CreateView):
    """Create a new transcription object"""
    model = Transcription
    template_name = 'transcriptions/create.html'
    fields = ['name', 'audio_file', 'url', 'project', 'transcription_item_publish_date']

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.pk},
            )

    def form_valid(self, form):
        """save the object and start the transcription"""
        form.instance.owner = self.request.user
        object = form.save()
        object.start_transcription()
        return super().form_valid(form)

    def get_form_class(self):
        """Apply custom widgets to the form and filter out projects that not
        owned by user"""
        form = super().get_form_class()

        # Name and URL need input class 'input' for Bulma.io
        form.base_fields['name'].widget = forms.TextInput(
            attrs={
                'class': 'input is-primary',
                'placeholder': 'Transcription Name',
                },
            )
        form.base_fields['url'].widget = forms.TextInput(
                attrs={
                    'class': 'input is-primary',
                    'placeholder': 'URL',
                    },
                )

        # Filter projects to only show those owned by user
        form.base_fields['project'] = forms.ModelChoiceField(
            queryset=Project.objects.filter(
                owner=self.request.user
                ),
            empty_label="Select a Project",
            )
        form.base_fields['transcription_item_publish_date'].widget=forms.SelectDateWidget(
                    years = list(
                        range(2000, datetime.datetime.now().year + 1))[::-1],
                    empty_label=(
                        'Select Year', 'Select Month', 'Select Day'),
                    )
        return form


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
        obj = self.get_object()
        updates = TranscriptionEdit.objects.filter(
                transcription=obj,
                status='pending_approval',
            )

        if obj.owner == self.request.user:
            context['transcription'] = obj.transcription_text

            if updates:
                context['update_message'] = 'pending'
            

        elif (my_updates := list(
            filter(lambda x:x.created_by == self.request.user, updates))):
            context['transcription'] = my_updates[0].transcription_text
            context['update_message'] = 'viewing'

        else:
            context['transcription'] = obj.transcription_text

        context['subscription'] = is_premium(self.request.user)
        return context


    def get_object(self):
        pk = self.kwargs['pk']
        obj = Transcription.objects.get(pk=pk)
        status = obj.status

        if status.lower() == 'in_progress':
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
    template_name = 'update-text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transcription'] = Transcription.objects.get(
                pk = self.kwargs.get('transcription_pk')
                )
        context['subscription'] = is_premium(self.request.user)
        return context

    def get_initial(self):
        initial = super().get_initial()
        if (pending_updates := list(
                filter(
                    lambda x:x.created_by, 
                    self.request.user)):
        initial['transcription_text'] = Transcription.objects.get(
                pk = self.kwargs.get('transcription_pk'),
                ).transcription_text
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.transcription = Transcription.objects.get(
                pk=self.kwargs.get('transcription_pk'))
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.kwargs.get('transcription_pk')},
            )


class TranscriptionTextModeratedUpdateView(
        LoginRequiredMixin,
        UserPassesTestMixin,
        UpdateView,
        ):

    model = Transcription
    template_name = 'update-text.html'
    fields = ['transcription_text']
    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'transcription_detail',
            kwargs={'pk': self.object.project.pk},
            )

    def test_func(self):
        return self.get_object().owner == self.request.user

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


