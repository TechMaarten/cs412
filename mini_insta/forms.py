"""Create a forms for new posts"""
from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    image_url = forms.URLField()
    class Meta:
        model = Post
        fields = ["caption"]
        