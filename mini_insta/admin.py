from django.contrib import admin
from .models import Profile, Photo, Post

'''Register Profile model'''
admin.site.register(Profile)

admin.site.register(Post)

admin.site.register(Photo)