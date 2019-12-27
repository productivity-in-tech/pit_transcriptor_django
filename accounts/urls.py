from django.urls import path

from . import views

urlpatterns = [
        path('signup/', views.SignUp.as_view(), name='signup'),
        path(
            'profile/<int:pk>/',
            views.UserDetailView.as_view(),
            name='user_detail',
            ),
        ]
