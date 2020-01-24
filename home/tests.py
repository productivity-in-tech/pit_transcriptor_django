from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from . import views
from projects.models import Project, ProjectsFollowing
from transcriptions.models import Transcription

# Create your tests here.


class HomePageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='test_user',
                password='test_password')
        project = Project.objects.create(
                name='Test_HomePage_Following_Project',
                )
        self.following_transcription = Transcription.objects.create(
                name='test_homepage_following_project_transcription',
                project=project,
                owner=self.user,
                audio_file = None,
                )
        self.latest_transcription = Transcription.objects.create(
                name='test_homepage_latest_transcription',
                project=project,
                audio_file = None,
                )

        ProjectsFollowing.objects.create(
                project=project,
                user=self.user,
                )

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


    def test_view_transcriptions_from_projects_following(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertIn(
                self.following_transcription,
                response.context_data['following_transcriptions'],
                )
        self.assertIn(
                self.following_transcription,
                response.context_data['latest_transcriptions'],
                )
        self.assertIn(
                self.latest_transcription,
                response.context_data['latest_transcriptions'],
                )
        self.assertEquals(response.status_code, 200)

