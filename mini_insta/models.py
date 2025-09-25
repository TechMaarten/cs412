from django.db import models

"""Created the class Profile"""
class Profile(models.Model):
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField()
    bio_text = models.TextField()
    join_date = models.DateField()

    #string to return the username
    def __str__(self):
        return self.username

