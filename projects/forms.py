import datetime
from django import forms
from django.db import models
from .models import Project

class ProjectDetailForm(forms.ModelForm):
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
                        'style': 'margin: 1em;',
                        },
                    ),
                'url': forms.TextInput(
                    attrs={
                        'class': 'input', 
                        'style': 'margin: 1em;',
                        },
                    )
                }

    def as_div(self):
        "Return this form rendered as HTML <div>s."
        return self._html_output(
            normal_row='''<div class="field">
            <div class="control">
            %(label)s%(field)s%(help_text)s
            </div>
            </div>''',
            error_row='%s',
            row_ender='</div>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True,
        )

