"""Maarten Lopes, lopesmaa@bu.edu"""
"""Helper for Login authentication"""
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.urls import reverse_lazy

class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin for requiring login and getting logged-in profile"""
    login_url = reverse_lazy("login")

    def get_logged_in_profile(self):
        """Return the Profile linked to the logged-in User"""
        if not self.request.user.is_authenticated:
            return None
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return None
