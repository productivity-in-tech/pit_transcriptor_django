import djstripe.models

def is_premium(user):
    if user.is_authenticated:
        plan = djstripe.models.Plan.objects.get(nickname='Transcription Test')

        if plan:
            stripe_customer = djstripe.models.Customer.objects.get(subscriber=user)
            return djstripe.models.Subscription.objects.filter(
                customer=stripe_customer,
                status='active',
                plan=plan,
                )

