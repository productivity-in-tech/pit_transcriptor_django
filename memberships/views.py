from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.template.response import TemplateResponse
import stripe
import djstripe.models
import djstripe.settings

from django.views.generic import FormView
from . import forms

# Create your views here.

class RegisterProMembership(FormView):
    template_name = 'register.html'
    form_class = forms.PurchaseSubscriptionForm

    def get_context_data(self, **kwargs):
        plan = djstripe.models.Plan.objects.get(nickname='Transcription Test')
        customer, created = djstripe.models.Customer.get_or_create(
                subscriber=self.request.user)
        session = stripe.checkout.Session.create(
                payment_method_types=['card'], 
                customer=customer.id,
                subscription_data={
                    'items': [{
                        'plan': 'plan_GaHwW4hWKKaxks', # Plan ID
                        }]},
                api_key=djstripe.settings.STRIPE_SECRET_KEY,
                success_url= 'http://transcriptor.productivityintech.com:5000',
                cancel_url= 'http://transcriptor.productivityintech.com:5000',
                )
        context = super().get_context_data(**kwargs)
        context['session_id'] = session['id']
        context['STRIPE_PUBLIC_KEY'] = djstripe.settings.STRIPE_PUBLIC_KEY
        return context

