import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'create/',
            views.TranscriptionCreateView.as_view(),
            name='transcription_create'),
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
            'update-text/<int:transcription_pk>',
            views.TranscriptionTextCreateView.as_view(),
            name='transcription_update_text'),
        path(
            'delete/<int:pk>',
            views.TranscriptionDeleteView.as_view(),
            name='transcription_delete'),
        path(
            'mod/update-text/<int:pk>',
            views.TranscriptionTextModeratedUpdateView.as_view(),
            name='transcription_mod_update_text'),
        path(
            'mod/approve/<int:pk>',
            views.TranscriptionTextModeratedApprovalView.as_view(),
            name='transcription_mod_approve_text'),
        path(
            'bulk-replace/<int:pk>',
            views.bulk_replace,
            name='transcription_bulk_replace_text'),
        ]
