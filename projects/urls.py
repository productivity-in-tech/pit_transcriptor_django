import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'detail/<int:pk>',
            views.ProjectDetailView.as_view(),
            name='project_detail',
            ),
        path(
            'create/',
            views.ProjectCreateView.as_view(),
            name='project_create',
            ),
        path(
            'follow/<int:pk>',
            views.follow_project,
            name='project_follow',
            ),
        path(
            'unfollow/<int:pk>',
            views.unfollow_project,
            name='project_unfollow',
            ),
        path(
            'update/<int:pk>',
            views.ProjectUpdateView.as_view(),
            name='project_update',
            ),
        path(
            'rss_update/<int:pk>',
            views.ProjectRSSUploadView.as_view(),
            name='project_rss_upload',
            ),
        path(
            'list/user',
            views.UserProjectListView.as_view(),
            name='user_project_list',
            ),
        path('list/following',
            views.UserProjectsFollowedListView.as_view(),
            name='user_project_following',
            ),
        ]

