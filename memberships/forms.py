from django import forms
import djstripe.models

class PurchaseSubscriptionForm(forms.Form):

    stripe_source = forms.CharField(
        max_length="255", widget=forms.HiddenInput(), required=False
    )


class PaymentIntentForm(forms.Form):
    pass

