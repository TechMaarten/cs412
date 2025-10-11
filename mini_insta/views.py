"""Maarten Lopes, lopesmaa@bu.edu"""
"""""mini_insta/views.py"""""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse 
from django.shortcuts import get_object_or_404
from .forms import CreatePostForm, UpadateProfileForm

class ProfileListView(ListView):
    """Create ProfileListView class"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'

class ProfileDetailView(DetailView):
    """Create ProfileDetailView class"""
    model = Profile
    template_name = 'mini_insta/show_profile.html'

class PostDetailView(DetailView):
    """Create PostDetailView class"""
    model = Post 
    template_name = 'mini_insta/show_post.html'

class CreatePostView(CreateView):
    """Create PostDetailView class"""
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    #adds a profile context so the template knows which profile the post is for
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile,pk=self.kwargs["pk"])
        context["profile"] = profile
        return context
    
    def form_valid(self, form):
        profile = get_object_or_404(Profile,pk=self.kwargs["pk"])
        post = form.save(commit=False)
        post.profile = profile
        post.save()

        #create a photo
        files = self.request.FILES.getlist("files")
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("show_post", args=[self.object.pk])

class UpdateProfileView(UpdateView):
    """Create UpdateProfileView class"""
    model = Profile
    form_class = UpadateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):
    """Create DeletePostView class"""
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        return reverse ('show_profile', args = [str(self.object.profile.pk)])
    
class UpdatePostView(UpdateView):
    """Create UpdatePostView class"""
    model = Post
    fields = ['caption']
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        return reverse ('show_post', args = [str(self.object.pk)])
