import os

from django.contrib import admin
from .models import Prestazione

class PrestazioneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'operator_name', 'note', 'file_display')  # Aggiunta dei campi 'operator_name'
    list_filter = ('note',)  # Filtri laterali per la lista delle prestazioni
    search_fields = ('note',)  # Campo di ricerca per la lista delle prestazioni

    def user_name(self, obj):
        if obj.utente:
            return obj.utente.username
        else:
            return "Nessun utente"
    user_name.short_description = 'Utente'  # Nome visualizzato nell'admin

    def operator_name(self, obj):
        if obj.operatore:
            return obj.operatore.username
        else:
            return "Nessun operatore"
    operator_name.short_description = 'Operatore'  # Nome visualizzato nell'admin

    def file_display(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)  # Estrae solo il nome del file
        else:
            return "Nessun file"
    file_display.short_description = 'File'  # Nome visualizzato nell'admin

admin.site.register(Prestazione, PrestazioneAdmin)
