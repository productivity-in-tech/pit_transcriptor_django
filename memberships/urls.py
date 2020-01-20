import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'register/',
            views.RegisterProMembership.as_view(),
            name='transcription_create'),
    ]
