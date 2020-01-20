from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone



# Create your models here.

UserModel = get_user_model()

class Membership(models.Model):
    user = models.OneToOneField(UserModel, on_delete = models.CASCADE)
    subscribedSince = models.DateTimeField(default=timezone.now)
    stripe_customer_id = models.CharField(max_length=250)
