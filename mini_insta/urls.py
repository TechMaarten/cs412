"""Maarten Lopes, lopesmaa@bu.edu"""
"""mini_insta/urls.py"""
from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView, UpdateProfileView, DeletePostView, UpdatePostView

"""Create urlpatterns"""
urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("profile/<int:pk>/update_post", UpdatePostView.as_view(), name="update_post"),
]
