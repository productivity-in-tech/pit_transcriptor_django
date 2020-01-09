from django.shortcuts import render
from rest_framework import generics, permissions

from .permissions import IsOwnerOrReadOnly
from .serializers import TranscriptionSerializer, ProjectSerializer
from transcriptions.models import Transcription
from projects.models import Project

# Create your views here.
class TranscriptionList(generics.ListCreateAPIView):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TranscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly]

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
            IsOwnerOrReadOnly]

