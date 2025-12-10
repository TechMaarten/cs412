"""
CS412 Final Project - Travel Planner Author: Maarten (lopesmaa@bu.edu)
Forms for the Travel Planner application.
"""

from django import forms
from .models import Trip, Destination, Activity, PackingItem


class TripForm(forms.ModelForm):
    """Form for creating and updating Trip objects"""
    class Meta:
        model = Trip
        fields = ["title", "start_date", "end_date", "description"]


class DestinationForm(forms.ModelForm):
    """Form for creating and updating Destination objects"""
    class Meta:
        model = Destination
        fields = ["city", "country", "arrival_date", "departure_date", "notes"]


class ActivityForm(forms.ModelForm):
    """Form for creating and updating Activity objects"""
    class Meta:
        model = Activity
        fields = ["name", "date", "time", "category", "cost", "description"]


class PackingItemForm(forms.ModelForm):
    """Form for creating and updating PackingItem objects"""
    class Meta:
        model = PackingItem
        fields = ["item_name", "quantity", "packed", "notes"]


class ActivitySearchForm(forms.Form):
    """
    Form used to filter and search Activities
    This is not tied to a specific model
    """
    trip = forms.ModelChoiceField(
        queryset=Trip.objects.all(),
        required=False,
        help_text="Filter by trip",
    )
    category = forms.CharField(
        max_length=100,
        required=False,
        help_text="Filter by category (e.g., sightseeing, food)",
    )
    min_cost = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        help_text="Minimum cost",
    )
    max_cost = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        required=False,
        help_text="Maximum cost",
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
