from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
from main.models import Profile
from main.tasks import import_random_users
from django.conf import settings

class HomeViewGetTests(TestCase):
    def setUp(self):
        for i in range(settings.CHUNK_SIZE + 5):
            Profile.objects.create(
                gender='M',
                first_name=f'First{i}',
                last_name=f'Last{i}',
                phone_number='123456789',
                email=f'user{i}@example.com',
                country='Country',
                city='City',
                street_number='10',
                street_name='Street',
                photo_url='http://example.com/photo.jpg',
            )
        self.client = Client()

    def test_home_get_renders_and_pagination(self):
        url = reverse('homepage')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)

        page_obj = response.context['page_obj']

        self.assertLessEqual(len(page_obj.object_list), settings.CHUNK_SIZE)
        first_user = Profile.objects.first()
        self.assertIn(first_user, page_obj.object_list)

class HomeViewPostTests(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('main.views.import_random_users.delay')
    def test_home_post_starts_tasks_and_redirects(self, mock_delay):
        url = reverse('homepage')
        count = settings.CHUNK_SIZE * 3 + 5

        response = self.client.post(url, {'count': str(count)})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

        expected_calls = (count + settings.CHUNK_SIZE - 1) // settings.CHUNK_SIZE
        self.assertEqual(mock_delay.call_count, expected_calls)

        expected_args = []
        remaining = count
        for _ in range(expected_calls):
            chunk = min(remaining, settings.CHUNK_SIZE)
            expected_args.append(chunk)
            remaining -= chunk

        actual_args = [call.args[0] for call in mock_delay.call_args_list]
        self.assertEqual(actual_args, expected_args)

class UserDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Profile.objects.create(
            gender='M',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            email='john@example.com',
            country='USA',
            city='NY',
            street_name='Main St',
            street_number='10',
            photo_url='http://example.com/photo.jpg'
        )

    def test_user_detail_existing_user(self):
        url = reverse('user_detail', args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.email)

    def test_user_detail_non_existing_user(self):
        url = reverse('user_detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class RandomUserViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_random_user_with_no_profiles(self):
        url = reverse('random_user')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 500)

    def test_random_user_with_profiles(self):
        Profile.objects.create(
            gender='M',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            email='john@example.com',
            country='USA',
            city='NY',
            street_name='Main St',
            street_number='10',
            photo_url='http://example.com/photo.jpg'
        )
        Profile.objects.create(
            gender='F',
            first_name='Jane',
            last_name='Smith',
            phone_number='0987654321',
            email='jane@example.com',
            country='USA',
            city='LA',
            street_name='Second St',
            street_number='20',
            photo_url='http://example.com/photo2.jpg'
        )

        url = reverse('random_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'John' in response.content.decode() or
            'Jane' in response.content.decode()
        )