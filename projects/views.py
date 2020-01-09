from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.shortcuts import render, redirect

from .models import Project, ProjectsFollowing
from .forms import ProjectDetailForm, RSSFeedProcessForm 
from .helpers import feed_core_data

from transcriptions.models import Transcription

# Create your views here.

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectDetailForm
    success_url = reverse_lazy('project_detail')
    template_name = 'projects/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('project_detail',
                kwargs={'pk':self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectDetailForm
    template_name = 'projects/update.html'

    success_url = reverse_lazy('project_detail')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('project_detail',
                kwargs={'pk':self.object.pk})


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transcriptions'] = Transcription.objects.filter(
                project=context['object']) 
        context['following'] = ProjectsFollowing.objects.filter(
                project=self.kwargs.get('pk'),
                user=self.request.user,
                )
        return context


@login_required
def follow_project(request, pk):
    project = ProjectsFollowing.objects.create(
            project = Project.objects.get(pk=pk),
            user = request.user
            )
    return redirect('project_detail', pk=pk)

@login_required
def unfollow_project(request, pk):
    project = ProjectsFollowing.objects.get(
            project = Project.objects.get(pk=pk),
            user = request.user
            ).delete()
    return redirect('project_detail', pk=pk)


class UserTemplateView(LoginRequiredMixin, FormView):
    template_name = 'confirm_rss_upload.html'
    form_class = RSSFeedProcessForm
    success_url = 'project_detail'

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        project.update(rss_feed_item_data=feed_core_data(project.rss_feed_url))
        return super().form_valid(form)
