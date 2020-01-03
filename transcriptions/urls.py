import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'create/',
            views.TranscriptionCreateView.as_view(),
            name='transcription_new'),
        path(
            'detail/<int:pk>',
            views.TranscriptionDetailView.as_view(),
            name='transcription_detail'),
        path(
            'update/<int:pk>',
            views.TranscriptionUpdateView.as_view(),
            name='transcription_update',
            ),
        path(
            'start/<int:pk>',
            views.start_transcription,
            name='start_transcription'),
        path(
            '<int:transcription_pk>/update-text/',
            views.TranscriptionTextCreateView.as_view(),
            name='transcriptiontext_create'),
        ]
