"""mini_insta/models.py"""
from django.db import models
from django.utils import timezone

"""Created the class Profile"""
class Profile(models.Model):
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

#post class
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} on {self.timestamp.strftime('%d-%m-%Y')}"
    
    #function to get all the photos
    def get_all_photos(self):
        return Photo.objects.filter(post=self).order_by("timestamp")
    
#photo class
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Photo for Post {self.post.id}"
    

