"""Import"""
import os
from django.contrib import admin
from django.utils.html import format_html

from .models import Prestazione


class PrestazioneAdmin(admin.ModelAdmin):
    """Classe admin per la gestione delle prestazioni"""
    list_display = ('pk', 'user_name', 'operator_name', 'short_note', 'file_display')
    list_filter = ('note',)
    search_fields = ('note',)
    actions = ['delete_model']

    def user_name(self, obj):
        """Metodo che restituisce il nome utente"""
        if obj.utente:
            return obj.utente.nome
        return "Nessun utente"

    user_name.short_description = 'Utente'

    def operator_name(self, obj):
        """Metodo che restituisce il nome utente dell'operatore sanitario"""
        if obj.operatore:
            return obj.operatore.nome
        return "Nessun operatore"

    operator_name.short_description = 'Operatore'

    def short_note(self, obj):
        """Metodo che restituisce la nota"""
        return obj.note[:20] if obj.note else 'Nessuna nota'

    short_note.short_description = 'Note'

    def file_display(self, obj):
        """Metodo che restituisce il file associato"""
        if obj.file:
            file_url = obj.file.url
            return format_html('<a href="{}" target="_blank">Visualizza</a>', file_url)
        return "Nessun file"

    file_display.short_description = 'File'

    # Togliamo l'azione di default
    def get_actions(self, request):
        """Metodo per disabilitare la funzione di default"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Metodo di delete personalizzato
    def delete_model(self, request, obj):
        """Metodo che elimina le istanze selezionate"""
        # Verifica se obj è un'istanza singola o un insieme di istanze
        if hasattr(obj, '__iter__'):
            # Si tratta di un insieme di istanze
            for prestazione in obj:
                if prestazione.file:
                    if os.path.isfile(prestazione.file.path):
                        os.remove(prestazione.file.path)
                prestazione.delete()
            self.message_user(request,
                              "Le prestazioni selezionate sono state eliminate con successo con i file associati.")
        else:
            # Si tratta di un'istanza singola
            if obj.file:
                if os.path.isfile(obj.file.path):
                    os.remove(obj.file.path)
            obj.delete()
            self.message_user(request, "La prestazione è stata eliminata con successo con il file associato.")

    delete_model.short_description = "Elimina le prestazioni selezionate con i file associati"


admin.site.register(Prestazione, PrestazioneAdmin)
