"""Maarten Lopes, lopesmaa@bu.edu"""
"""voter_analytics/forms.py"""
from django import forms

class VoterFilterForm(forms.Form):
    party_choices = [
        ('', 'Any'),
        ('D', 'Democrat'),
        ('R', 'Republican'),
        ('U', 'Unenrolled'),
    ]

    voter_score_choices = [(i, i) for i in range(6)]

    party = forms.ChoiceField(choices=party_choices, required=False)
    min_birth_year = forms.IntegerField(label="Born After (Year)", required=False)
    max_birth_year = forms.IntegerField(label="Born Before (Year)", required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + voter_score_choices, required=False)

    v20state = forms.BooleanField(label="Voted in 2020 State?", required=False)
    v21town = forms.BooleanField(label="Voted in 2021 Town?", required=False)
    v21primary = forms.BooleanField(label="Voted in 2021 Primary?", required=False)
    v22general = forms.BooleanField(label="Voted in 2022 General?", required=False)
    v23town = forms.BooleanField(label="Voted in 2023 Town?", required=False)
