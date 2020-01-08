from django.shortcuts import render
from rest_framework import generics

from .serializers import TranscriptionSerializer, ProjectSerializer
from transcriptions.models import Transcription
from projects.models import Project

# Create your views here.
class TranscriptionList(generics.ListCreateAPIView):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer


class TranscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

