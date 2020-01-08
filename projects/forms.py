import datetime
from django import forms
from customModelForm import CustomModelForm
from django.db import models
from .models import Project

class ProjectDetailForm(CustomModelForm):
    class Meta:
        model = Project
        fields = (
                'name',
                'url',
                )
        widgets = {
                'name': forms.TextInput(
                    attrs={
                        'class': 'input', 
                        },
                    ),
                'url': forms.TextInput(
                    attrs={
                        'class': 'input', 
                        },
                    )
                } 
