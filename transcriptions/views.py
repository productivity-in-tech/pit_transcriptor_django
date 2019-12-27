from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Transcription, TranscriptionText, Project
from .forms import TranscriptionAddForm, ProjectAddForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your views here.
def transcription_list(request):
    transcriptions = Transcription.objects.all()

    return render(request, 'transcriptions/transcription_list.html',
            {'transcriptions': transcriptions})

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_transcriptions'] = Transcription.objects.all()[:5]
        context['latest_projects'] = Project.objects.all()[:5]
        return context

class TranscriptionDetailView(DetailView):
    model = Transcription
    template_name = 'transcriptions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version_count'] = TranscriptionText.objects.filter(
                transcription=context['transcription'],
                ).count()
        return context

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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@require_http_methods(["POST"])
def start_transcription(request, pk):
    transcription = Transcription.objects.get(pk=pk)
    transcription.start_transcription()
    transcription.status = 'in_progress'
    return redirect('transcription_detail', pk=pk)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'projects/create.html'
    fields = [
            'name',
            'url',
            'can_edit',
            ]
    success_url = reverse_lazy('project_detail')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('project_detail',
                kwargs={'pk':self.object.pk})


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transcriptions'] = Transcription.objects.filter(
                project=context['object']) 
        return context


class ProjectListView(ListView):
    model = Project
    paginate_by = 10
    template_name = "projects/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if user_id := self.request.GET.get('by_user'):
            context['owner'] = User.objects.get(pk=user_id)
        return context

    def get_queryset(self):
        if self.request.GET.get('by_user'):
            filter_user = self.request.GET.get('by_user')
            return Project.objects.filter(owner=filter_user)

        else:
            return Project.objects.all() 
