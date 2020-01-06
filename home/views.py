from itertools import chain
from django.db.models import Q
from django.views.generic.base import TemplateView
from projects.models import Project, ProjectsFollowing
from transcriptions.models import Transcription
# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            following_projects_ids = ProjectsFollowing.objects.filter(
                    user=self.request.user).values_list('project', flat=True)
            user_projects_ids = Project.objects.filter(
                    owner=self.request.user).values_list('pk', flat=True)

            following_transcriptions = Transcription.objects.filter(
                    Q(project__in=following_projects_ids) |
                    Q(project__in=user_projects_ids))
            context['following_transcriptions'] = following_transcriptions[:5]
            context['latest_transcriptions'] = Transcription.objects.all()[:5]
            

        context['latest_projects'] = Project.objects.all()[:5]
        return context

