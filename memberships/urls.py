import django.contrib.auth.urls
from django.urls import path, include

from . import views

urlpatterns = [
        path(
            'register/',
            views.RegisterProMembership.as_view(),
            name='pro_register'),
    ]
