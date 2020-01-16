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
from django.http import HttpResponseRedirect

from django_q.tasks import async_task, result

from .models import Project, ProjectsFollowing
from .forms import ProjectDetailForm, RSSFeedProcessForm 
from .helpers import transcription_get_or_create

from transcriptions.models import Transcription

# Create your views here.
class UserProjectsFollowedListView(LoginRequiredMixin, ListView):
    """Return a List of all the Projects that the Logged in User Follows"""
    model = ProjectsFollowing
    template_name = 'list_following.html'
    context_object_name = 'projects'

    def post(self, request, *args, **kwargs):
        unfollow_item = filter(lambda x:'unfollow' in x, request.POST)
        pk = int(next(unfollow_item).strip('unfollow-'))
        ProjectsFollowing.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse('user_project_following'))

    def get_queryset(self):
        return ProjectsFollowing.objects.filter(user=self.request.user)

class UserProjectListView(LoginRequiredMixin, ListView):
    """Return a List of Projects Belonging to the Current User"""
    model = Project
    template_name = 'list_user.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

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


class ProjectRSSUploadView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'confirm_rss_upload.html'
    form_class = RSSFeedProcessForm


    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs.get('pk'))
        
        for feed_item in project.feed_data:
            async_task(
                    transcription_get_or_create,
                    feed_item=feed_item,
                    project=project,
                    )

        return super().form_valid(form)

    

    def get_success_url(self, **kwargs):
        return reverse_lazy('project_detail',
                kwargs={'pk': self.kwargs.get('pk')})
        
