# main/tasks.py
import requests
from celery import shared_task


@shared_task
def import_random_users(count):
    from .models import Profile
    response = requests.get(f"https://randomuser.me/api/?results={count}")
    if response.status_code == 200:
        data = response.json()
        for user in data["results"]:
            email = user["email"]
            Profile.objects.get_or_create(
                email=email,
                defaults={
                    "gender": user["gender"][0].upper(),
                    "first_name": user["name"]["first"],
                    "last_name": user["name"]["last"],
                    "phone_number": user["phone"],
                    "country": user["location"]["country"],
                    "city": user["location"]["city"],
                    "street_name": user["location"]["street"]["name"],
                    "street_number": str(user["location"]["street"]["number"]),
                    "photo_url": user["picture"]["medium"],
                },
            )
