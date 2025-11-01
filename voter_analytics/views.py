"""Maarten Lopes, lopesmaa@bu.edu"""
"""voter_analytics/views.py"""
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
import pandas as pd

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data
            if data.get('party'):
                queryset = queryset.filter(party=data['party'])
            if data.get('min_birth_year'):
                queryset = queryset.filter(date_of_birth__year__gte=data['min_birth_year'])
            if data.get('max_birth_year'):
                queryset = queryset.filter(date_of_birth__year__lte=data['max_birth_year'])
            if data.get('voter_score'):
                queryset = queryset.filter(voter_score=data['voter_score'])
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if data.get(field):
                    queryset = queryset.filter(**{field: True})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'

    def get_queryset(self):
        view = VoterListView()
        view.request = self.request
        return view.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        #explicitly list fields to ensure they appear
        df = pd.DataFrame(list(voters.values(
            'date_of_birth', 'party',
            'v20state', 'v21town', 'v21primary', 'v22general', 'v23town'
        )))

        #Defensive: if the dataframe is empty, skip plots
        if df.empty:
            context['birth_chart'] = "<p>No data available for selected filters.</p>"
            context['party_chart'] = ""
            context['participation_chart'] = ""
            return context

        # --- Birth Year Histogram ---
        df['birth_year'] = pd.to_datetime(df['date_of_birth']).dt.year
        fig1 = px.histogram(df, x='birth_year', title="Voters by Year of Birth")
        context['birth_chart'] = fig1.to_html(full_html=False)

        # --- Party Pie Chart ---
        fig2 = px.pie(df, names='party', title="Party Affiliation Distribution")
        context['party_chart'] = fig2.to_html(full_html=False)

        # --- Election Participation ---
        participation = {
            '2020 State': df['v20state'].sum(),
            '2021 Town': df['v21town'].sum(),
            '2021 Primary': df['v21primary'].sum(),
            '2022 General': df['v22general'].sum(),
            '2023 Town': df['v23town'].sum(),
        }
        fig3 = px.bar(
            x=list(participation.keys()),
            y=list(participation.values()),
            title="Election Participation Counts"
        )
        context['participation_chart'] = fig3.to_html(full_html=False)

        context['form'] = VoterFilterForm(self.request.GET)
        return context
