import djstripe.models

def is_customer(user):
    if user.is_authenticated:
        stripe_customer = djstripe.models.Customer.objects.filter(subscriber=user)

        if stripe_customer:
            return True

        else:
            return False

    else:
        return False



def is_premium(user):
        plan = djstripe.models.Plan.objects.get(nickname='Transcription Test')

        if plan and is_customer(user):
            stripe_customer = djstripe.models.Customer.objects.get(subscriber=user)
            return djstripe.models.Subscription.objects.filter(
                customer=stripe_customer,
                status='active',
                plan=plan,
                )

        else:
            return []
