from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import HealthCareUser


class HealthCareUserAdmin(UserAdmin):
    pass


admin.site.register(HealthCareUser)
