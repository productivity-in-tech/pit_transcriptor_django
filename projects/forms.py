from django.utils.translation import gettext_lazy as _

import datetime
from django import forms
from customModelForm import CustomModelForm
from django.db import models
from .models import Project

class ProjectModelForm(CustomModelForm):
    class Meta:
        model = Project
        fields = []


class ProjectDetailForm(ProjectModelForm):
    class Meta:
        model = Project
        fields = (
               'name',
                'url',
                'rss_feed_url',
                'project_image',
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
                'rss_feed_url': forms.TextInput(
                    attrs={
                        'class': 'input', 
                        },
                    ),
                }
        labels = {
                'rss_feed_url': _('RSS Feed URL'),
                } 
        help_text = {
                'rss_feed_url': _('The URL of your projects RSS Feed. Used to \
                    autoimport projects')
                }


class RSSFeedProcessForm(ProjectModelForm):
    pass
