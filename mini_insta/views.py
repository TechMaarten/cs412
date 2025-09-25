from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

"""Create ProfileListView class"""
class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'

"""Create ProfileDetailView class"""
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
