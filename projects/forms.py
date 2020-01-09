from django.utils.translation import gettext_lazy as _

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
                'rss_feed',
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
                    ),
                'rss_feed': forms.TextInput(
                    attrs={
                        'class': 'input', 
                        },
                    ),
                }
        labels = {
                'rss_feed': _('RSS Feed URL'),
                } 
        help_text = {
                'rss_feed': _('The URL of your projects RSS Feed. Used to \
                    autoimport projects')

                }
