from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'email', 'gender', 'phone_number', 'get_location')
    search_fields = ('first_name', 'last_name', 'email')
# Register your models here.
