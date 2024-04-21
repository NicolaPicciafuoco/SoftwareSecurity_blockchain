from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from core.group_get_queryset import return_queryset_terapia
from core.group_name import (GROUP_PAZIENTE,
                             GROUP_CAREGIVER,
                             GROUP_DOTTORE,
                             GROUP_DOTTORE_SPECIALISTA,
                             GROUP_AMMINISTRATORE)
from .models import Terapia
from Management_User.models import HealthCareUser
import os
from django.db import IntegrityError
from django.http import HttpResponseRedirect


class TerapiaAdmin(admin.ModelAdmin):
    ''' Classe per strutturare la vista admin '''
    model = Terapia
    list_display = ['user_name', 'note', 'prescrittore_name', 'visualizza_file', ]
    # search_fields = ['prescrittore', 'note', 'hash']
    readonly_fields = ['hash']
    actions = ['delete_model']

    def get_list_display(self, request):
        if request.user.groups.all().first().name == GROUP_PAZIENTE:
            return ['prescrittore_name', 'note', 'visualizza_file', 'hash']
        else:
            return ['user_name', 'note', 'prescrittore_name', 'visualizza_file']

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.prescrittore == request.user:
            return True
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        return return_queryset_terapia(self, request, TerapiaAdmin)

    def user_name(self, obj):
        ''' Funzione per restituire lo username del paziente'''
        if obj.utente:
            return obj.utente.nome
        return "Nessun utente"
    user_name.short_description = 'Paziente'

    def prescrittore_name(self, obj):
        ''' Funzione per restituire lo username dell'prescrittore'''
        if obj.prescrittore:
            return obj.prescrittore.nome
        return "Nessun operatore"
    prescrittore_name.short_description = 'Prescrittore'

    def visualizza_file(self, obj):
        ''' Funzione per visualizzare i file'''
        if obj.file:
            file_url = obj.file.url
            return format_html('<a href="{}" target="_blank">Visualizza</a>', file_url)
        return "Nessun file"

    visualizza_file.short_description = "File"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj:
            try:
                obj.check_json_integrity()
                messages.success(request, f"Terapia {obj} verificata.")
            except IntegrityError as e:
                messages.error(request, f"Errore durante la verifica della {obj}: {e}")
                form_url_prec = request.META.get('HTTP_REFERER')
                return HttpResponseRedirect(form_url_prec)
        return super().change_view(request, object_id, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        """ sovrascrivere form"""
        form = super().get_form(request, obj, **kwargs)
        user_group = request.user.groups.all().first().name
        utenti = HealthCareUser.objects.filter(
            groups=Group.objects.get(name=GROUP_PAZIENTE).id
        )
        utenti_f = utenti.filter(in_cura_da__id=request.user.id)
        prescrittori = HealthCareUser.objects.filter(
            groups__in=[
                Group.objects.get(name=GROUP_DOTTORE).id,
                Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA).id
            ]
        )
        if obj is None:
            # la terapia non è ancora stata creata => è una CREATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['prescrittore'].choices = [(p.id, p.show(request=request)) for p in prescrittori] + [(request.user.id, request.user.show(request=request)),]
                form.base_fields['prescrittore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti]

            elif user_group in [GROUP_PAZIENTE, GROUP_CAREGIVER]:
                form.base_fields['prescrittore'].widget.attrs['style'] = 'display: none;'

            elif user_group == GROUP_DOTTORE:
                form.base_fields['prescrittore'].choices = [(request.user.id, request.user.show(request=request)), ]
                form.base_fields['prescrittore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti_f]

            elif user_group == GROUP_DOTTORE_SPECIALISTA:
                form.base_fields['prescrittore'].choices = [(request.user.id, request.user.show(request=request)), ]
                form.base_fields['prescrittore'].initial = request.user
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti_f]
        else:
            # la terapia è stata creata => è un UPDATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['prescrittore'].choices = [(p.id, p.show(request=request)) for p in prescrittori] + [(obj.prescrittore.id, obj.prescrittore.show(request=request)),]
                form.base_fields['prescrittore'].initial = obj.prescrittore
                form.base_fields['utente'].choices = [(u.id, u.show(request=request)) for u in utenti]
                form.base_fields['utente'].initial = obj.utente
            else:
                try:
                    form.base_fields['prescrittore'].choices = [(obj.prescrittore.id, obj.prescrittore.show(request=request)), ]
                    form.base_fields['utente'].choices = [(obj.utente.id, obj.utente.show(request=request)), ]
                except Exception:
                    pass

        return form

    def get_actions(self, request):
        ''' Sovrascrive l'azione di delate di default'''
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if request.user.groups.all().first().name == GROUP_PAZIENTE:
            del actions['delete_model']
        return actions

    def delete_model(self, request, obj):
        ''' Funzione sovrascritta per eliminare le terapie'''
        if request.user.groups.all().first().name == GROUP_PAZIENTE:
            self.message_user(request,
                              "il paziente non può compiere questa azione ")
        else:
            if hasattr(obj, '__iter__'):
                for terapia in obj:
                    if terapia.file:
                        if os.path.isfile(terapia.file.path):
                            os.remove(terapia.file.path)
                    terapia.delete()
                self.message_user(request,
                                  "Le terapie selezionate sono"
                                  " state eliminate con successo con i file associati.")
            else:
                if obj.file:
                    if os.path.isfile(obj.file.path):
                        os.remove(obj.file.path)
                obj.delete()
                self.message_user(request,
                                  "La Terapia è stata eliminata con successo "
                                  "con il file associato.")
    delete_model.short_description = "Elimina le terapie selezionate con i file associati"


admin.site.register(Terapia, TerapiaAdmin)
