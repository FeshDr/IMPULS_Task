from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
from main.models import Profile
from main.tasks import import_random_users


class ImportRandomUsersTaskTest(TestCase):

    @patch("main.tasks.requests.get")
    def test_import_random_users_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "email": "test1@example.com",
                    "gender": "male",
                    "name": {"first": "John", "last": "Doe"},
                    "phone": "123456789",
                    "location": {
                        "country": "CountryX",
                        "city": "CityY",
                        "street": {"name": "StreetZ", "number": 12}
                    },
                    "picture": {"medium": "http://example.com/photo.jpg"},
                },
                {
                    "email": "test2@example.com",
                    "gender": "female",
                    "name": {"first": "Jane", "last": "Smith"},
                    "phone": "987654321",
                    "location": {
                        "country": "CountryA",
                        "city": "CityB",
                        "street": {"name": "StreetC", "number": 34}
                    },
                    "picture": {"medium": "http://example.com/photo2.jpg"},
                },
            ]
        }
        mock_get.return_value = mock_response

        import_random_users(2)

        self.assertEqual(Profile.objects.count(), 2)
        profile1 = Profile.objects.get(email="test1@example.com")
        self.assertEqual(profile1.first_name, "John")
        self.assertEqual(profile1.gender, "M")
        profile2 = Profile.objects.get(email="test2@example.com")
        self.assertEqual(profile2.first_name, "Jane")
        self.assertEqual(profile2.gender, "F")

    @patch("main.tasks.requests.get")
    def test_import_random_users_api_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        import_random_users(1)

        self.assertEqual(Profile.objects.count(), 0)