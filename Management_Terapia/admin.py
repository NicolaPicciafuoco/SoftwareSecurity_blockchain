from django.contrib import admin
from .models import Terapia
# Register your models here.
class TerapiaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Terapia, TerapiaAdmin)