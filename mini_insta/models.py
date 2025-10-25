"""Maarten Lopes, lopesmaa@bu.edu"""
"""mini_insta/models.py"""
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    """Created the class Profile"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    bio_text = models.TextField()
    join_date = models.DateField()

    #string to return the username
    def __str__(self):
        return self.username
    
    #function to get all posts
    def get_all_posts(self):
        return Post.objects.filter(profile=self).order_by("-timestamp")
    
    def get_absolute_url(self):
        return reverse("show_profile", args=[str(self.pk)])
    
    def get_followers(self):
        follows = Follow.objects.filter(profile=self)
        return [f.follower_profile for f in follows]

    def get_num_followers(self):
        return len(self.get_followers())

    def get_following(self):
        follows = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in follows]

    def get_num_following(self):
        return len(self.get_following())
    
    def get_post_feed(self):
        following_profiles = [f.profile for f in Follow.objects.filter(follower_profile=self)]
        return Post.objects.filter(profile__in=following_profiles).order_by("-timestamp")

class Post(models.Model):
    """Created the Post class"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} on {self.timestamp.strftime('%d-%m-%Y')}"
    
    #function to get all the photos
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")
    
    def get_all_comments(self):
        return Comment.objects.filter(post=self)

    def get_likes(self):
        return Like.objects.filter(post=self)
    
class Photo(models.Model):
    """Created the Photo class"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    image_file = models.ImageField(upload_to="photos", blank=True, null=True)

    def __str__(self):
        if self.image_url:
            return f"Photo for Post {self.post.id}"
        else:
            return f"Photo for Post {self.post.id}"
    
    
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url

class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile.display_name} liked Post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return f"{self.profile.display_name} commented: {self.text[:25]}"
