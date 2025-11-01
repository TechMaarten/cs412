"""Maarten Lopes, lopesmaa@bu.edu"""
"""voter_analytics/models.py"""
from django.db import models
import csv

class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apt_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party = models.CharField(max_length=2)
    precinct = models.CharField(max_length=10)

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

""" CSV Import Helper Function """
def load_data(csv_path):
    """ Imports voter data from the Newton CSV file into the Django database """
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                first_name=row["First Name"],
                last_name=row["Last Name"],
                street_number=row["Residential Address - Street Number"],
                street_name=row["Residential Address - Street Name"],
                apt_number=row["Residential Address - Apartment Number"],
                zip_code=row["Residential Address - Zip Code"],
                date_of_birth=row["Date of Birth"],
                date_of_registration=row["Date of Registration"],
                party=row["Party Affiliation"].strip(),
                precinct=row["Precinct Number"],
                v20state=row["v20state"] == "TRUE",
                v21town=row["v21town"] == "TRUE",
                v21primary=row["v21primary"] == "TRUE",
                v22general=row["v22general"] == "TRUE",
                v23town=row["v23town"] == "TRUE",
                voter_score=int(row["voter_score"])
            )
