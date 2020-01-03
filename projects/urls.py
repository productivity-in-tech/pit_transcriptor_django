import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'detail/<int:pk>',
            views.ProjectDetailView.as_view(),
            name='project_detail'),
        path(
            'create/',
            views.ProjectCreateView.as_view(),
            name='project_create'),
        ]
