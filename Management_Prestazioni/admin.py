"""
Gestione della pagina admin del modello Prestazione e connessi
"""
import os
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from Management_User.models import HealthCareUser
from core.group_name import (GROUP_PAZIENTE,
                             GROUP_CAREGIVER,
                             GROUP_DOTTORE,
                             GROUP_DOTTORE_SPECIALISTA,
                             GROUP_AMMINISTRATORE)
from core.group_get_queryset import return_queryset_prestazione
from .models import Prestazione


class PrestazioneAdmin(admin.ModelAdmin):
    """Classe admin per la gestione delle prestazioni"""
    model = Prestazione
    list_display = ('pk', 'user_name', 'operator_name', 'short_note', 'file_display')
    list_filter = ('note',)
    search_fields = ('note',)
    actions = ['delete_model']

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.operatore == request.user:
            return True
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        return return_queryset_prestazione(self, request, PrestazioneAdmin)

    def get_form(self, request, obj=None, **kwargs):
        """ sovrascrivere form"""
        form = super().get_form(request, obj, **kwargs)
        user_group = request.user.groups.all().first().name
        utenti = HealthCareUser.objects.filter(
            groups=Group.objects.get(name=GROUP_PAZIENTE).id
        )
        operatori = HealthCareUser.objects.filter(
            groups__in=[
                Group.objects.get(name=GROUP_CAREGIVER).id,
                Group.objects.get(name=GROUP_DOTTORE).id,
                Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA).id
            ]
        )
        if obj is None:
            # la terapia non è ancora stata creata => è una CREATE
            gruppi_operatori = [
                GROUP_DOTTORE,
                GROUP_DOTTORE_SPECIALISTA,
                GROUP_CAREGIVER
            ]
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['operatore'].choices = [
                                                            (p.id, p.show(request=request)) for p in operatori
                                                        ] + [(request.user.id, request.user.show(request=request)),]
                form.base_fields['operatore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti]

            elif user_group == GROUP_PAZIENTE:
                form.base_fields['operatore'].widget.attrs['style'] = 'display: none;'

            elif user_group in gruppi_operatori:
                form.base_fields['operatore'].choices = [(request.user.id, request.user.show(request=request)), ]
                form.base_fields['operatore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti]
        else:
            # la terapia è stata creata => è un UPDATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['operatore'].choices = [
                                                            (p.id, p.show(request=request)) for p in operatori
                                                        ] + [(obj.operatore.id, obj.operatore.show(request=request)),]
                form.base_fields['operatore'].initial = obj.operatore
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti]
                form.base_fields['utente'].initial = obj.utente
            else:
                try:
                    form.base_fields['operatore'].choices = [(obj.operatore.id, obj.operatore.show(request=request)), ]
                    form.base_fields['utente'].choices = [(obj.utente.id, obj.utente.show(request=request)), ]
                except Exception:
                    pass
        return form

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
            return format_html(
                '<a href="{}" target="_blank">Visualizza</a>', file_url)
        return "Nessun file"
    file_display.short_description = 'File'

    def get_actions(self, request):
        """Metodo per disabilitare la funzione di default"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        """Metodo che elimina le istanze selezionate personalizzato"""
        if hasattr(obj, '__iter__'):
            for prestazione in obj:
                if prestazione.file:
                    if os.path.isfile(prestazione.file.path):
                        os.remove(prestazione.file.path)
                prestazione.delete()
            self.message_user(
                request,
                "Le prestazioni selezionate sono state eliminate con successo con i file associati."
            )
        else:
            if obj.file:
                if os.path.isfile(obj.file.path):
                    os.remove(obj.file.path)
            obj.delete()
            self.message_user(
                request,
                "La prestazione è stata eliminata con successo con il file associato."
            )
    delete_model.short_description = "Elimina le prestazioni selezionate con i file associati"


admin.site.register(Prestazione, PrestazioneAdmin)
