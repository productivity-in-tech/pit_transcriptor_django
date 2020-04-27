from django.contrib.auth.mixins import AccessMixin
from premium_check import is_premium

class UserIsPremiumMixin:
    '''
    View Mixin that creates the "is_premium" context
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_premium'] = is_premium(user)
        return context


