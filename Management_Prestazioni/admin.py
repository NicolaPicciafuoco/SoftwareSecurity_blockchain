from django.contrib import admin
from .models import Prestazione

class PrestazioneAdmin(admin.ModelAdmin):
    pass


admin.site.register(Prestazione, PrestazioneAdmin)