from django.views.generic.base import TemplateView
from projects.models import Project, ProjectsFollowing
from transcriptions.models import Transcription
# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            followed_projects = ProjectsFollowing.objects.filter(user=self.request.user).all()
            context['followed_projects'] = followed_projects

        context['latest_transcriptions'] = Transcription.objects.all()[:5]
        context['latest_projects'] = Project.objects.all()[:5]
        return context

