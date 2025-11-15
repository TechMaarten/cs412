"""Maarten Lopes, lopesmaa@bu.edu"""
"""dadjokes/urls.py"""
from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.index),
    path('random', views.random_view),
    path('jokes', views.jokes_list),
    path('joke/<int:pk>', views.joke_detail),
    path('pictures', views.pictures_list),
    path('picture/<int:pk>', views.picture_detail),

    path('api/', api_views.api_random),
    path('api/random', api_views.api_random),
    path('api/random_picture', api_views.api_random_picture),

    path('api/jokes', api_views.api_jokes),
    path('api/joke/<int:pk>', api_views.api_joke_detail),

    path('api/pictures', api_views.api_pictures),
    path('api/picture/<int:pk>', api_views.api_picture_detail),
]
