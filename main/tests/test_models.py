from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
from main.models import Profile
from main.tasks import import_random_users

class ProfileModelTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            gender='M',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            email='john.doe@example.com',
            country='CountryX',
            city='CityY',
            street_number='12A',
            street_name='Main Street',
            photo_url='http://example.com/photo.jpg'
        )

    def test_str_method(self):
        self.assertEqual(str(self.profile), "John Doe (john.doe@example.com)")

    def test_get_location_property(self):
        expected_location = "CountryX, CityY, Main Street 12A"
        self.assertEqual(self.profile.get_location, expected_location)

    def test_creation(self):
        profile = Profile.objects.get(email='john.doe@example.com')
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.phone_number, '1234567890')
        self.assertEqual(profile.photo_url, 'http://example.com/photo.jpg')