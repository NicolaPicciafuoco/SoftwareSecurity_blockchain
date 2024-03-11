import os
from django.contrib import admin
from django.forms import ModelForm
from django.utils.html import format_html

from .models import Terapia


class TerapiaAdminForm(ModelForm):
    ''' serve per sovrascrive le form di base'''

    class Meta:
        ''' serve per sovrascrivere le form di base'''
        model = Terapia
        fields = '__all__'


class TerapiaAdmin(admin.ModelAdmin):
    ''' classe per strutturare la vista admin'''
    form = TerapiaAdminForm
    list_display = ['note', 'user_name', 'prescrittore_name', 'visualizza_file', ]
    actions = ['delete_model']

    def user_name(self, obj):
        ''' funzione per restituire lo username del paziente'''
        if obj.utente:
            return obj.utente.nome
        return "Nessun utente"

    def prescrittore_name(self, obj):
        ''' funzione per restituire lo username dell'prescrittore'''
        if obj.prescrittore:
            return obj.prescrittore.nome
        return "Nessun operatore"

    def visualizza_file(self, obj):
        ''' funzione per visualizzare i file'''
        if obj.file:
            file_url = obj.file.url
            return format_html('<a href="{}" target="_blank">Visualizza</a>', file_url)
        return "Nessun file"

    visualizza_file.short_description = "File"

    def get_form(self, request, obj=None, **kwargs):
        """ sovrascrivere form"""
        form = super().get_form(request, obj, **kwargs)
        # Disabilita la possibilità di scegliere il prescrittore nella form
        form.base_fields['prescrittore'].widget.attrs['disabled'] = True
        form.base_fields['prescrittore'].widget.attrs['style'] = 'display: none;'
        return form

    def get_actions(self, request):
        ''' sovrascrive l'azione di delate di default'''
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        ''' funzione sovrascritta per eliminare le terapie'''
        # Verifica se obj è un'istanza singola o un insieme di istanze
        if hasattr(obj, '__iter__'):
            # Si tratta di un insieme di istanze
            for terapia in obj:
                if terapia.file:
                    if os.path.isfile(terapia.file.path):
                        os.remove(terapia.file.path)
                terapia.delete()
            self.message_user(request,
                              "Le prestazioni selezionate sono"
                              " state eliminate con successo con i file associati.")
        else:
            # Si tratta di un'istanza singola
            if obj.file:
                if os.path.isfile(obj.file.path):
                    os.remove(obj.file.path)
            obj.delete()
            self.message_user(request,
                              "La prestazione è stata eliminata con successo "
                              "con il file associato.")

    delete_model.short_description = "Elimina le prestazioni selezionate con i file associati"


admin.site.register(Terapia, TerapiaAdmin)
