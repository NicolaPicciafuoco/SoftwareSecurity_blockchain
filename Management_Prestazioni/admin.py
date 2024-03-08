from django.contrib import admin
from .models import Prestazione

class PrestazioneAdmin(admin.ModelAdmin):
    list_display = ('id', 'note', 'file_display')  # Campi da visualizzare nella lista delle prestazioni
    list_filter = ('note',)  # Filtri laterali per la lista delle prestazioni
    search_fields = ('note',)  # Campo di ricerca per la lista delle prestazioni

    def file_display(self, obj):
        if obj.file:
            return obj.file.name
        else:
            return "Nessun file"
    file_display.short_description = 'File'  # Personalizza l'intestazione della colonna

admin.site.register(Prestazione, PrestazioneAdmin)
