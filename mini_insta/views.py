"""Maarten Lopes, lopesmaa@bu.edu"""
"""""mini_insta/views.py"""""
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse 
from django.shortcuts import get_object_or_404
from .forms import CreatePostForm, UpadateProfileForm
from django.db.models import Q

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
    
class ShowFollowersDetailView(DetailView):
    """Create ShowFollowersDetailView class"""
    model = Profile
    template_name = "mini_insta/show_followers.html"

class ShowFollowingDetailView(DetailView):
    """Create ShowFollowingDetailView class"""
    model = Profile
    template_name = "mini_insta/show_following.html"

class PostFeedListView(ListView):
    """Create PostFeedListView class"""
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context
    
class SearchView(ListView):
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        if not query:
            profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        # ✅ Find posts that match the search text OR belong to matching profiles
        matching_profiles = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        return Post.objects.filter(
            Q(caption__icontains=query) | Q(profile__in=matching_profiles)
        ).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])

        context["profile"] = profile
        context["query"] = query
        # show matching profiles separately as well
        context["matching_profiles"] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        return context