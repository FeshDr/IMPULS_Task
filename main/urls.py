from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('random/', views.random_user, name='random_user'),
]
