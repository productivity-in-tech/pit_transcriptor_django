from django import forms

class CustomModelForm(forms.ModelForm):
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
