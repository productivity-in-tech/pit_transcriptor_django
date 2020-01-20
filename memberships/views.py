from django.shortcuts import render
from django.template.response import TemplateResponse
import djstripe.models
import djstripe.settings

from django.views.generic import FormView
from . import forms

# Create your views here.

class RegisterProMembership(FormView):
    template_name = 'register.html'
    form_class = forms.PurchaseSubscriptionForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = djstripe.settings.STRIPE_PUBLIC_KEY
        return context



    def form_valid(self, form):
        stripe_source = form.cleaned_data["stripe_source"]
        plan = djstripe.models.Plan.objects.get(nickname='Transcription Test')

        user = self.request.user
        if not user.is_authenticated:
            return

        customer, created = djstripe.models.Customer.get_or_create(subscriber=user)
        customer.add_card(stripe_source) 

        stripe_subscription = stripe.Subscription.create(
                customer = customer.id,
                items=[{"plan": plan.id}],
                billing="charge_automatically",
                api_key=djstripe.settings.STRIPE_SECRET_KEY,
        )

        subscription = djstripe.models.Subscription.sync_from_stripe_data(
                stripe_subscription,
                )
        
        self.request.subscription = subscription

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts_detail',
                kwargs={'pk': user.pk},
                )


def create_payment_intent(request):
    if request.method == "POST":
        intent = None
        data = json.loads(request.body)
        try:
            if "payment_method_id" in data:
                # Create the PaymentIntent
                intent = stripe.PaymentIntent.create(
                    payment_method=data["payment_method_id"],
                    amount=1099,
                    currency="usd",
                    confirmation_method="manual",
                    confirm=True,
                    api_key=djstripe.settings.STRIPE_SECRET_KEY,
                )
            elif "payment_intent_id" in data:
                intent = stripe.PaymentIntent.confirm(
                    data["payment_intent_id"],
                    api_key=djstripe.settings.STRIPE_SECRET_KEY,
                )
        except stripe.error.CardError as e:
            # Display error on client
            return_data = json.dumps({"error": e.user_message}), 200
            return HttpResponse(
                return_data[0], content_type="application/json", status=return_data[1]
            )

        if (
            intent.status == "requires_action"
            and intent.next_action.type == "use_stripe_sdk"
        ):
            # Tell the client to handle the action
            return_data = (
                json.dumps(
                    {
                        "requires_action": True,
                        "payment_intent_client_secret": intent.client_secret,
                    }
                ),
                200,
            )
        elif intent.status == "succeeded":
            # The payment did not need any additional actions and completed!
            # Handle post-payment fulfillment
            return_data = json.dumps({"success": True}), 200
        else:
            # Invalid status
            return_data = json.dumps({"error": "Invalid PaymentIntent status"}), 500
        return HttpResponse(
            return_data[0], content_type="application/json", status=return_data[1]
        )

    else:
        ctx = {"STRIPE_PUBLIC_KEY": djstripe.settings.STRIPE_PUBLIC_KEY}
        return TemplateResponse(request, "payment_intent.html", ctx)


