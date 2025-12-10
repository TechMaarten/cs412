"""CS412 Final Project - Travel Planner Author: Maarten (lopesmaa@bu.edu)
    Data models for a travel planning application. Users can create trips, add destinations within each trip, 
    schedule activities at each destination and manage packing items for each trip"""

from django.db import models

class Trip(models.Model):
    """A Trip represents one full travel plan. This model stands on its own and does not depend on any other model
    Other models (Destination, PackingItem) will reference Trip via ForeignKey"""
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable representation of the Trip"""
        return f"{self.title} ({self.start_date} → {self.end_date})"

    class Meta:
        ordering = ["start_date", "title"]
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

class Destination(models.Model):
    """A Destination represents a city or stop within a Trip"""

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="destinations",
        help_text="The trip that this destination belongs to.",
    )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.city}, {self.country} ({self.trip.title})"

    class Meta:
        ordering = ["trip", "arrival_date", "city"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

class Activity(models.Model):
    """An Activity is something scheduled at a given Destination"""
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="activities",
        help_text="The destination where this activity takes place.",
    )
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    category = models.CharField(
        max_length=100,
        help_text="Example categories: sightseeing, food, nightlife, travel, etc.",
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Estimated cost in USD.",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} @ {self.destination.city} on {self.date}"

    class Meta:
        ordering = ["date", "time", "name"]
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

class PackingItem(models.Model):
    """A PackingItem represents something that should be packed for a Trip"""
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="packing_items",
        help_text="The trip this item is being packed for.",
    )
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    packed = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    def __str__(self):
        """Return a readable representation of the packing item"""
        return f"{self.item_name} x{self.quantity} for {self.trip.title}"

    class Meta:
        ordering = ["trip", "packed", "item_name"]
        verbose_name = "Packing Item"
        verbose_name_plural = "Packing Items"
