"""Create a forms for new posts"""
from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    """created the PostForm class"""
    class Meta:
        model = Post
        fields = ["caption"]
