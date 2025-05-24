import requests
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile
from .tasks import import_random_users
from django.conf import settings
import random
# Create your views here.

def home(request):
    if request.method == "POST":
        count = int(request.POST.get("count", 1))
        while count > 0:
            request_cnt = min(count, settings.CHUNK_SIZE)
            import_random_users.delay(request_cnt)
            count -= request_cnt
        return redirect("homepage")

    users = Profile.objects.all().order_by("id")
    paginator = Paginator(users, settings.CHUNK_SIZE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "main/main.html", {"page_obj": page_obj})


def user_detail(request, pk):
    user = get_object_or_404(Profile, pk=pk)
    return render(request, "main/user_detail.html", {"user": user})


def random_user(request):
    users_count = Profile.objects.count()
    if users_count == 0:
        return render(request, 'main/error.html', {'message': 'Нет пользователей в базе'})
    random_index = random.randint(0, users_count - 1)
    user = Profile.objects.all()[random_index]

    return render(request, 'main/user_detail.html', {'user': user})
