import django.contrib.auth.urls
from django.urls import path, include

from transcriptions import views

urlpatterns = [
        path('', views.HomePageView.as_view(), name='home'),
        path(
            'transcription/create/',
            views.TranscriptionCreateView.as_view(),
            name='transcription_new'),
        path(
            'transcription/detail/<int:pk>',
            views.TranscriptionDetailView.as_view(),
            name='transcription_detail'),
        path(
            'transcription/update/<int:pk>',
            views.TranscriptionUpdateView.as_view(),
            name='transcription_update',
            ),
        path(
            'transcription/start/<int:pk>',
            views.start_transcription,
            name='start_transcription'),
        path(
            'project/detail/<int:pk>',
            views.ProjectDetailView.as_view(),
            name='project_detail'),
        path(
            'projects/',
            views.project_list,
            name='project_list',
            ),
        path(
            'project/create/',
            views.ProjectCreateView.as_view(),
            name='project_create'),
        ]
