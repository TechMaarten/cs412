"""Maarten Lopes, lopesmaa@bu.edu"""
from django.contrib import admin
from .models import Profile, Photo, Post, Comment, Follow, Like

'''Register Profile model'''
admin.site.register(Profile)

admin.site.register(Post)

admin.site.register(Photo)

admin.site.register(Follow)

admin.site.register(Comment)

admin.site.register(Like)