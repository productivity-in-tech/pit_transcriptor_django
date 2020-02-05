from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from transcriptions.models import Transcription
from projects.models import Project, ProjectsFollowing
from django.core.mail import send_mail
from django.template.loader import render_to_string
import djstripe.models
from premium_check import is_premium


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def send_confirmation(self):
        subject = "New Account Created - PIT Transcriptor"
        from_email = "noreply@discourse.productivityintech.com"
        to_email = self.cleaned_data['email']
        message = render_to_string('email_confirmation.txt',
                {'username':self.cleaned_data['username']})
        html_message = render_to_string('email_confirmation.html',
                {'username':self.cleaned_data['username']})

        send_mail(
            subject=subject,
            from_email=from_email,
            recipient_list=[to_email],
            message=message,
            html_message=html_message,
            )

        

# Create your views here
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = "detail.html"

    def test_func(self):
        return self.kwargs['pk'] == self.request.user.pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = is_premium(self.request.user)
        context['projects'] = Project.objects.filter(owner=self.request.user) 
        context['latest_transcriptions'] = Transcription.objects.filter(owner=self.request.user)[:5]
        context['following'] = ProjectsFollowing.objects.filter(
                user=self.request.user, 
                )
        return context
