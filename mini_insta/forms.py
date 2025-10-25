"""Maarten Lopes, lopesmaa@bu.edu"""
"""Create a forms for new posts"""
from django import forms
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    """created the PostForm class"""
    class Meta:
        model = Post
        fields = ["caption"]

class UpadateProfileForm(forms.ModelForm):
    """ created the UpdateProfileForm class """
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["username", "display_name", "bio_text", "profile_image_url"]