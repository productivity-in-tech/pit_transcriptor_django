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
            'update-text/<int:pk>',
            views.TranscriptionTextUpdateView.as_view(),
            name='transcription_update_text'),
        path(
            'bulk-replace/<int:pk>',
            views.bulk_replace,
            name='transcription_bulk_replace_text'),
        ]
