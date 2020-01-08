from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
        path('transcription/', views.TranscriptionList.as_view()),
        path('transcription/<int:pk>', views.TranscriptionDetail.as_view()),
        path('project/', views.ProjectList.as_view()),
        path('project/<int:pk>', views.ProjectDetail.as_view()),
        ]

urlpatters = format_suffix_patterns(urlpatterns)
