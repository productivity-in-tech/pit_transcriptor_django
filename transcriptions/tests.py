from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from . import views
from .models import Transcription
from projects.models import Project, ProjectsFollowing


class TranscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username='test_user',
                password='test_password')
        project = Project.objects.create(
                name='Test_HomePage_Following_Project'
                )
        self.client.login(username='test_user', password='test_password')
        self.my_transcription = Transcription.objects.create(
                name='test_homepage_following_project_transcription',
                project=project,
                owner=self.user,
                audio_file = None,
                )

    def test_User_transcription_list(self):
        url_response = self.client.get('/transcription/list/')
        self.assertEquals(url_response.status_code, 200)
        reverse_response = self.client.get(reverse('user_transcription_list'))
        self.assertEquals(reverse_response.status_code, 200)

    def test_User_transcription_list_shows_transcriptions_not_in_projects(self):
        response = self.client.get('/transcription/list/')
        self.assertIn(
                self.my_transcription,
                response.context_data['transcription_list'],
                )

    def test user_proposed_edit(self):
        pass

