"""""mini_insta/views.py"""""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from django.urls import reverse 
from django.shortcuts import get_object_or_404
from .forms import CreatePostForm

"""Create ProfileListView class"""
class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'

"""Create ProfileDetailView class"""
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'

"""Create PostDetailView class"""
class PostDetailView(DetailView):
    model = Post 
    template_name = 'mini_insta/show_post.html'

"""Create PostDetailView class"""
class CreatePostView(CreateView):
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
        image_url = self.request.POST.get("image_url")
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("show_post", args=[self.object.pk])
