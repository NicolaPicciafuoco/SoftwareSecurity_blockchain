from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from core.group_get_queryset import return_queryset_terapia
from core.group_name import *
from .models import Terapia
from Management_User.models import HealthCareUser
import os


class TerapiaAdmin(admin.ModelAdmin):
    ''' classe per strutturare la vista admin'''
    model = Terapia
    list_display = ['note', 'user_name', 'prescrittore_name', 'visualizza_file', ]
    actions = ['delete_model']

    def get_queryset(self, request):
        return return_queryset_terapia(self, request, TerapiaAdmin)

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
        user_group = request.user.groups.all().first().name
        utenti = HealthCareUser.objects.filter(
            groups=Group.objects.get(name=GROUP_PAZIENTE).id
        )
        prescrittori = HealthCareUser.objects.filter(
            groups__in=[
                Group.objects.get(name=GROUP_DOTTORE).id,
                Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA).id
            ]
        )
        if obj is None:
            # la terapia non è ancora stata creata => è una CREATE
            if user_group == GROUP_AMMINISTRATORE:
                prescrittori.exclude(id=request.user.id)
                form.base_fields['prescrittore'].choices = [(p.id, p) for p in prescrittori] + [(request.user.id, request.user),]
                form.base_fields['prescrittore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u) for u in utenti]

            elif user_group in [GROUP_PAZIENTE, GROUP_CAREGIVER, GROUP_INFERMIERE]:
                form.base_fields['prescrittore'].widget.attrs['style'] = 'display: none;'

            elif user_group in [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA]:
                form.base_fields['prescrittore'].choices = [(request.user.id, request.user), ]
                form.base_fields['prescrittore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u) for u in utenti]
        else:
            # la terapia è stata creata => è un UPDATE
            prescrittori.exclude(id=obj.prescrittore.id)
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['prescrittore'].choices = [(p.id, p) for p in prescrittori] + [(obj.prescrittore.id, obj.prescrittore),]
                form.base_fields['prescrittore'].initial = obj.prescrittore
                form.base_fields['utente'].choices = [(u.id, u) for u in utenti]
                form.base_fields['utente'].initial = obj.utente
            else:
                form.base_fields['prescrittore'].choices = [(obj.prescrittore.id, obj.prescrittore), ]
                form.base_fields['utente'].choices = [(obj.utente.id, obj.utente), ]

        return form

    def get_actions(self, request):
        ''' sovrascrive l'azione di delate di default'''
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def delete_model(self, request, obj):
        ''' funzione sovrascritta per eliminare le terapie'''
        if hasattr(obj, '__iter__'):
            for terapia in obj:
                if terapia.file:
                    if os.path.isfile(terapia.file.path):
                        os.remove(terapia.file.path)
                terapia.delete()
            self.message_user(request,
                              "Le prestazioni selezionate sono"
                              " state eliminate con successo con i file associati.")
        else:
            if obj.file:
                if os.path.isfile(obj.file.path):
                    os.remove(obj.file.path)
            obj.delete()
            self.message_user(request,
                              "La prestazione è stata eliminata con successo "
                              "con il file associato.")
    delete_model.short_description = "Elimina le prestazioni selezionate con i file associati"


admin.site.register(Terapia, TerapiaAdmin)
