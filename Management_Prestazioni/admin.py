import os

from django.contrib import admin
from .models import Prestazione

class PrestazioneAdmin(admin.ModelAdmin):
    list_display = ('pk','user_name','operator_name','short_note', 'file_display')  # Aggiunta dei campi 'operator_name'
    list_filter = ('note',)  # Filtri laterali per la lista delle prestazioni
    search_fields = ('note',)  # Campo di ricerca per la lista delle prestazioni

    def user_name(self, obj):
        if obj.utente:
            return obj.utente.nome
        else:
            return "Nessun utente"
    user_name.short_description = 'Utente'  # Nome visualizzato nell'admin

    def operator_name(self, obj):
        if obj.operatore:
            return obj.operatore.nome
        else:
            return "Nessun operatore"
    operator_name.short_description = 'Operatore'  # Nome visualizzato nell'admin


    def short_note(self, obj):
        # Mostra solo i primi 20 caratteri della nota
        return obj.note[:20] if obj.note else 'Nessuna nota'
    short_note.short_description = 'Note'  # Nome visualizzato nell'admin

    def file_display(self, obj):
        if obj.file:
            # Restituisce il nome del file senza estensione
            return os.path.splitext(os.path.basename(obj.file.name))[0]
        else:
            return "Nessun file"

    file_display.short_description = 'File'  # Nome visualizzato nell'admin
admin.site.register(Prestazione, PrestazioneAdmin)
