"""Admin configuration for the Travel Planner models. Registers Trip, Destination, Activity, and PackingItem with the 
Django admin."""

from django.contrib import admin
from .models import Trip, Destination, Activity, PackingItem

class DestinationInline(admin.TabularInline):
    model = Destination
    extra = 1

class PackingItemInline(admin.TabularInline):
    model = PackingItem
    extra = 1

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "start_date", "end_date")
    search_fields = ("title",)
    inlines = [DestinationInline, PackingItemInline]

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "trip", "arrival_date", "departure_date")
    list_filter = ("trip", "country")
    search_fields = ("city", "country", "trip__title")

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "date", "time", "category", "cost")
    list_filter = ("destination__trip", "category", "date")
    search_fields = ("name", "destination__city", "destination__trip__title")

@admin.register(PackingItem)
class PackingItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "trip", "quantity", "packed")
    list_filter = ("trip", "packed")
    search_fields = ("item_name", "trip__title")
