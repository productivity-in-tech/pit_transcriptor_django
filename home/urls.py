import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path('', views.HomePageView.as_view(), name='home'),
        path('about/', views.AboutPageView.as_view(), name='about'),
        path('model/', views.ModelPageView.as_view(), name='model'),
        ]
