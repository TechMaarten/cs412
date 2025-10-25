"""Maarten Lopes, lopesmaa@bu.edu"""
"""""mini_insta/views.py"""""
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from .models import Profile, Post, Photo, Like, Follow
from django.urls import reverse 
from django.shortcuts import get_object_or_404
from .forms import CreatePostForm, UpadateProfileForm, CreateProfileForm
from django.db.models import Q
from .mixins import MiniInstaLoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login


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

class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    """Create PostDetailView class"""
    model = Post
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    #adds a profile context so the template knows which profile the post is for
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_logged_in_profile()
        context["profile"] = profile
        return context
    
    def form_valid(self, form):
        profile = self.get_logged_in_profile()
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

class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    """Create UpdateProfileView class"""
    model = Profile
    form_class = UpadateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        return self.get_logged_in_profile()

class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
    """Create DeletePostView class"""
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        logged_in_profile = self.get_logged_in_profile()
        if post.profile != logged_in_profile:
            return redirect("show_post", pk=post.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse ('show_profile', args = [str(self.object.profile.pk)])
    
class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
    """Create UpdatePostView class"""
    model = Post
    fields = ['caption']
    template_name = 'mini_insta/update_post_form.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        logged_in_profile = self.get_logged_in_profile()
        if post.profile != logged_in_profile:
            # not your post — block edit/delete
            return redirect("show_post", pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

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

class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    """Create PostFeedListView class"""
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        profile = self.get_logged_in_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_logged_in_profile()
        context["profile"] = profile
        return context
    
class SearchView(MiniInstaLoginRequiredMixin, ListView):
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        if not query:
            profile = self.get_logged_in_profile()
            return render(request, "mini_insta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        # Find posts that match the search text OR belong to matching profiles
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
        profile = self.get_logged_in_profile()

        context["profile"] = profile
        context["query"] = query
        # show matching profiles separately as well
        context["matching_profiles"] = Profile.objects.filter(
            Q(username__icontains=query) |
            Q(display_name__icontains=query) |
            Q(bio_text__icontains=query)
        )
        return context
    
class ShowOwnProfileView(MiniInstaLoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"

    def get_object(self):
        return self.get_logged_in_profile()

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
class FollowProfileView(MiniInstaLoginRequiredMixin, TemplateView):
    """Logged-in user follows another profile"""
    def dispatch(self, request, *args, **kwargs):
        follower = self.get_logged_in_profile()
        to_follow = get_object_or_404(Profile, pk=self.kwargs["pk"])

        # Prevent following yourself
        if follower != to_follow:
            Follow.objects.get_or_create(profile=to_follow, follower_profile=follower)
        return HttpResponseRedirect(reverse("show_profile", args=[to_follow.pk]))

class DeleteFollowView(MiniInstaLoginRequiredMixin, TemplateView):
    """Logged-in user unfollows another profile"""
    def dispatch(self, request, *args, **kwargs):
        follower = self.get_logged_in_profile()
        to_unfollow = get_object_or_404(Profile, pk=self.kwargs["pk"])

        Follow.objects.filter(profile=to_unfollow, follower_profile=follower).delete()
        return HttpResponseRedirect(reverse("show_profile", args=[to_unfollow.pk]))

class LikePostView(MiniInstaLoginRequiredMixin, TemplateView):
    """Logged-in user likes a post"""
    def dispatch(self, request, *args, **kwargs):
        liker = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        # Prevent liking your own post
        if liker != post.profile:
            Like.objects.get_or_create(post=post, profile=liker)
        return HttpResponseRedirect(reverse("show_post", args=[post.pk]))

class DeleteLikeView(MiniInstaLoginRequiredMixin, TemplateView):
    """Logged-in user unlikes a post"""
    def dispatch(self, request, *args, **kwargs):
        liker = self.get_logged_in_profile()
        post = get_object_or_404(Post, pk=self.kwargs["pk"])

        Like.objects.filter(post=post, profile=liker).delete()
        return HttpResponseRedirect(reverse("show_post", args=[post.pk]))
    
class LogoutConfirmationView(TemplateView):
    template_name = "mini_insta/logged_out.html"