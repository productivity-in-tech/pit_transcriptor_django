import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path('', views.HomePageView.as_view(), name='home'),
        ]
