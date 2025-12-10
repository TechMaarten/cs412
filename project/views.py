"""
CS412 Final Project - Travel Planner Author: Maarten (lopesmaa@bu.edu)
Views for the Travel Planner application.
This file contains both class-based views 
and at least one function-based view (activity_report).
"""

from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Trip, Destination, Activity, PackingItem
from .forms import (
    TripForm,
    DestinationForm,
    ActivityForm,
    PackingItemForm,
    ActivitySearchForm,
)


class TripListView(ListView):
    """
    Display a list of all Trips.

    This view demonstrates the "read" operation for Trips
    """
    model = Trip
    template_name = "project/trip_list.html"
    context_object_name = "trips"


class TripDetailView(DetailView):
    """
    Display details for a single Trip, including its Destinations,
    Activities and Packing Items
    """
    model = Trip
    template_name = "project/trip_detail.html"
    context_object_name = "trip"

    def get_context_data(self, **kwargs):
        """Add related destinations, activities, and packing items"""
        context = super().get_context_data(**kwargs)
        trip = self.object
        context["destinations"] = trip.destinations.all()
        context["packing_items"] = trip.packing_items.all()
        return context



class TripCreateView(CreateView):
    """
    Create a new Trip
    Demonstrates the "create" operation using a generic class-based view
    """
    model = Trip
    form_class = TripForm
    template_name = "project/trip_form.html"

    def get_success_url(self):
        """Redirect to the detail view for the newly created Trip"""
        return reverse("project:trip_detail", args=[self.object.pk])


class TripUpdateView(UpdateView):
    """Update an existing Trip"""
    model = Trip
    form_class = TripForm
    template_name = "project/trip_form.html"

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.pk])


class TripDeleteView(DeleteView):
    """
    Delete a Trip
    Demonstrates the "delete" operation
    """
    model = Trip
    template_name = "project/confirm_delete.html"
    success_url = reverse_lazy("project:trip_list")



class DestinationCreateView(CreateView):
    """
    Create a new Destination that belongs to a specific Trip

    The Trip is determined by the URL parameter trip_pk
    """
    model = Destination
    form_class = DestinationForm
    template_name = "project/destination_form.html"

    def form_valid(self, form):
        trip = get_object_or_404(Trip, pk=self.kwargs["trip_pk"])
        form.instance.trip = trip
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])


class DestinationUpdateView(UpdateView):
    """Update an existing Destination"""
    model = Destination
    form_class = DestinationForm
    template_name = "project/destination_form.html"

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])


class DestinationDeleteView(DeleteView):
    """Delete a Destination"""
    model = Destination
    template_name = "project/confirm_delete.html"

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])



class ActivityCreateView(CreateView):
    """
    Create a new Activity belonging to a specific Destination
    The Destination is determined by the URL parameter destination_pk
    """
    model = Activity
    form_class = ActivityForm
    template_name = "project/activity_form.html"

    def form_valid(self, form):
        destination = get_object_or_404(Destination, pk=self.kwargs["destination_pk"])
        form.instance.destination = destination
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "project:trip_detail", args=[self.object.destination.trip.pk]
        )


class ActivityUpdateView(UpdateView):
    """Update an existing Activity"""
    model = Activity
    form_class = ActivityForm
    template_name = "project/activity_form.html"

    def get_success_url(self):
        return reverse(
            "project:trip_detail", args=[self.object.destination.trip.pk]
        )


class ActivityDeleteView(DeleteView):
    """Delete an Activity"""
    model = Activity
    template_name = "project/confirm_delete.html"

    def get_success_url(self):
        return reverse(
            "project:trip_detail", args=[self.object.destination.trip.pk]
        )




class PackingItemCreateView(CreateView):
    """
    Create a PackingItem for a specific Trip
    The Trip is determined by the URL parameter trip_pk
    """
    model = PackingItem
    form_class = PackingItemForm
    template_name = "project/packingitem_form.html"

    def form_valid(self, form):
        trip = get_object_or_404(Trip, pk=self.kwargs["trip_pk"])
        form.instance.trip = trip
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])


class PackingItemUpdateView(UpdateView):
    """Update an existing PackingItem"""
    model = PackingItem
    form_class = PackingItemForm
    template_name = "project/packingitem_form.html"

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])


class PackingItemDeleteView(DeleteView):
    """Delete a PackingItem"""
    model = PackingItem
    template_name = "project/confirm_delete.html"

    def get_success_url(self):
        return reverse("project:trip_detail", args=[self.object.trip.pk])




def activity_report(request):
    """
    Function-based view that implements searching and filtering Activities
    Users can filter by trip, category, cost range, and date range
    The view also computes the total cost of the filtered activities,
    which serves as a simple "report" on trip spending
    """
    form = ActivitySearchForm(request.GET or None)

    activities = Activity.objects.select_related("destination__trip").all()

    if form.is_valid():
        trip = form.cleaned_data.get("trip")
        category = form.cleaned_data.get("category")
        min_cost = form.cleaned_data.get("min_cost")
        max_cost = form.cleaned_data.get("max_cost")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")

        if trip:
            activities = activities.filter(destination__trip=trip)
        if category:
            activities = activities.filter(category__icontains=category)
        if min_cost is not None:
            activities = activities.filter(cost__gte=min_cost)
        if max_cost is not None:
            activities = activities.filter(cost__lte=max_cost)
        if start_date:
            activities = activities.filter(date__gte=start_date)
        if end_date:
            activities = activities.filter(date__lte=end_date)

    total_cost = activities.aggregate(total=Sum("cost"))["total"] or 0

    context = {
        "form": form,
        "activities": activities,
        "total_cost": total_cost,
    }
    return render(request, "project/activity_report.html", context)
