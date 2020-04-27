import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'create/',
            views.TranscriptionCreateView.as_view(),
            name='transcription_create'),
        path('list/',
            views.UserTranscriptionListView.as_view(),
            name='user_transcription_list'),
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
            views.TranscriptionTextCreateView.as_view(),
            name='transcription_request_update_text'),
        path(
            'delete/<int:pk>',
            views.TranscriptionDeleteView.as_view(),
            name='transcription_delete'),
        path(
            'bulk-replace/<int:pk>',
            views.bulk_replace,
            name='transcription_bulk_replace_text'),
        path('download_text/<int:pk>',
            views.download_transcription_text,
            name='download_transcription'),
        path('download_audio/<int:pk>',
            views.download_transcription_audio,
            name='download_transcription_audio'),
        path('transcription-edit/delete/<int:pk>',
            views.TranscriptionEditDeleteView.as_view(),
            name='transcription_edit_delete'),
        path('transcription-edit/list/',
            views.TranscriptionEditListView.as_view(),
            name='transcription_edit_list'),
        ]