from django.db import models

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street_number = models.CharField(max_length=20)
    street_name = models.CharField(max_length=50)
    photo_url = models.URLField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def get_location(self):
        return f"{self.country}, {self.city}, {self.street_name} {self.street_number}"