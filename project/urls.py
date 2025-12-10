"""
Maarten Lopes, lopesmaa@bu.edu
project/urls.py
"""

from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    # Trip URLs
    path("", views.TripListView.as_view(), name="trip_list"),
    path("trip/add/", views.TripCreateView.as_view(), name="trip_add"),
    path("trip/<int:pk>/", views.TripDetailView.as_view(), name="trip_detail"),
    path("trip/<int:pk>/edit/", views.TripUpdateView.as_view(), name="trip_edit"),
    path("trip/<int:pk>/delete/", views.TripDeleteView.as_view(), name="trip_delete"),

    # Destination URLs
    path(
        "trip/<int:trip_pk>/destinations/add/",
        views.DestinationCreateView.as_view(),
        name="destination_add",
    ),
    path(
        "destination/<int:pk>/edit/",
        views.DestinationUpdateView.as_view(),
        name="destination_edit",
    ),
    path(
        "destination/<int:pk>/delete/",
        views.DestinationDeleteView.as_view(),
        name="destination_delete",
    ),

    # Activity URLs
    path(
        "destination/<int:destination_pk>/activities/add/",
        views.ActivityCreateView.as_view(),
        name="activity_add",
    ),
    path(
        "activity/<int:pk>/edit/",
        views.ActivityUpdateView.as_view(),
        name="activity_edit",
    ),
    path(
        "activity/<int:pk>/delete/",
        views.ActivityDeleteView.as_view(),
        name="activity_delete",
    ),

    # Packing item URLs
    path(
        "trip/<int:trip_pk>/packing/add/",
        views.PackingItemCreateView.as_view(),
        name="packing_add",
    ),
    path(
        "packing/<int:pk>/edit/",
        views.PackingItemUpdateView.as_view(),
        name="packing_edit",
    ),
    path(
        "packing/<int:pk>/delete/",
        views.PackingItemDeleteView.as_view(),
        name="packing_delete",
    ),

    # Activity report / search
    path("activities/report/", views.activity_report, name="activity_report"),
]
