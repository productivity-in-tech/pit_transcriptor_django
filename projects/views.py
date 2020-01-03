from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Project

from transcriptions.models import Transcription

# Create your views here.

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
    template_name = "detail.html"

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
