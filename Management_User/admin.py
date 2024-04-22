"""
In questo file viene svolta la definizione del codice per la pagina del utente custom
"""
from web3 import Account
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from core.group_get_queryset import return_queryset_user
from core.group_name import (GROUP_CAREGIVER,
                             GROUP_DOTTORE,
                             GROUP_DOTTORE_SPECIALISTA,
                             GROUP_PAZIENTE,
                             GROUP_AMMINISTRATORE)
from .models import HealthCareUser


class HealthCareUserAdmin(UserAdmin):
    """Definizione di cio che puo vedere e fare l'utente
     quando va nella pagina di amministrazione dell'utente"""
    model = HealthCareUser
    list_display = ['nome',
                    'str_role',
                    'sesso',
                    'email',
                    'data_nascita',
                    'wallet_address']
    ordering = ['nome',
                'cognome',
                'sesso',
                'data_nascita',
                'wallet_address']
    search_fields = ['nome']
    filter_horizontal = ['in_cura_da', 'groups']

    def has_change_permission(self, request, obj=None):
        """Cambia i permessi in base al utente che accede"""
        if obj is not None and obj.pk == request.user.pk:
            return True
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        """Modifica qaunti utente un utente che accede può visualizzare"""
        return return_queryset_user(self, request, HealthCareUserAdmin)

    def get_readonly_fields(self, request, obj=None):
        """Seleziona quali fields possono essere solo letti"""
        return [
            'data_modifica',
            'data_creazione',
            'wallet_address',
            'is_superuser',
            'is_staff',
            'private_key',
            'last_login',
        ] if request.user.groups.all().first().name == GROUP_AMMINISTRATORE \
            else [
            'data_modifica',
            'data_creazione',
            'last_login',
            'wallet_address',
            'private_key',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'assistito',
            'in_cura_da',
        ]

    def get_exclude(self, request, obj=None):
        """Esclude oppure no sia il campo assistito sia quello di in_cura_da"""
        lista = []
        if request.user.groups in [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_PAZIENTE]:
            lista.append('assistito')
        if request.user.groups in [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_CAREGIVER]:
            lista.append('in_cura_da')
        return lista

    def str_role(self, obj):
        """Ritorna il gruppo di appartenenza"""
        try:
            first_element = obj.groups.first().name
            return str(first_element)
        except Exception:
            return "-"

    str_role.short_description = 'Ruolo'

    fieldsets = (
        (
            "Gestione Accessi", {
                "fields": ('password', 'last_login',
                           ('data_modifica', 'data_creazione'),),
                "classes": ("collapse",)
            }
        ),
        (
            "Informazione Personali", {
                'fields': ('email', ('nome', 'cognome', 'sesso'),
                           'data_nascita', 'luogo_nascita',
                           'telefono', 'codice_fiscale',
                           'indirizzo_residenza', 'indirizzo_domicilio',
                           'assistito', 'in_cura_da',
                           'wallet_address',),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff',
                           'is_superuser', 'groups'),
                "classes": ("collapse",)
            }
        ),
    )

    add_fieldsets = (
        (
            "Gestione Accessi", {
                "fields": ('email', 'password1', 'password2'),

            }
        ),
        (
            "Informazione Personali", {
                'fields': (('nome', 'cognome', 'sesso'),
                           ('data_nascita', 'luogo_nascita'),
                           'codice_fiscale', 'telefono',
                           'indirizzo_residenza', 'indirizzo_domicilio',
                           'assistito', 'in_cura_da',),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff',
                           'is_superuser', 'groups',),

            }
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """ sovrascrivere form"""
        form = super().get_form(request, obj, **kwargs)
        user_group = request.user.groups.all().first().name
        gruppi = Group.objects.exclude(name=GROUP_AMMINISTRATORE)
        pazienti = HealthCareUser.objects.filter(
            groups=Group.objects.get(name=GROUP_PAZIENTE).id
        )
        prescrittori = HealthCareUser.objects.filter(
            groups__in=[
                Group.objects.get(name=GROUP_DOTTORE).id,
                Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA).id
            ]
        )
        if obj is None:
            # l'utente non è ancora stato creata => è una CREATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['groups'].choices = [(g.id, g) for g in gruppi
                                                         ] + [
                    (Group.objects.get(name=GROUP_AMMINISTRATORE).id,
                     Group.objects.get(name=GROUP_AMMINISTRATORE)),
                ]
                form.base_fields['assistito'].choices = [('', "--------")] + [
                    (u.id, u.show(request=request)) for u in pazienti]
                form.base_fields['in_cura_da'].choices = [
                    (p.id, p.show(request=request)) for p in prescrittori]
        else:
            # l'utente è stato creata => è un UPDATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['groups'].choices = [(g.id, g) for g in gruppi
                                                      ] + [
                     (Group.objects.get(name=GROUP_AMMINISTRATORE).id,
                      Group.objects.get(name=GROUP_AMMINISTRATORE)),
                ]
                form.base_fields['assistito'].choices = [('', "--------")] + [
                    (u.id, u.show(request=request)) for u in pazienti]
                form.base_fields['in_cura_da'].choices = [
                    (p.id, p.show(request=request)) for p in prescrittori]
        return form

    def save_model(self, request, obj, form, change):
        if not change:
            account = Account.create()
            obj.wallet_address = account.address
            obj.private_key = account._private_key.hex()
            super().save_model(request, obj, form, change)
        if obj is not None:
            super().save_model(request, obj, form, change)


admin.site.register(HealthCareUser, HealthCareUserAdmin)
