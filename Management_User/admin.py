from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from core.group_get_queryset import return_queryset_user
from .models import HealthCareUser
from core.group_name import *
from web3 import Web3
from web3 import Account

from eth_account import account
class HealthCareUserAdmin(UserAdmin):
    model = HealthCareUser

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.pk == request.user.pk:
            return True
        return super().has_change_permission(request, obj)

    def get_queryset(self, request):
        return return_queryset_user(self, request, HealthCareUserAdmin)

    def get_readonly_fields(self, request, obj=None):
        return [
            'data_modifica',
            'data_creazione',
            'last_login',
        ] if request.user.groups.all().first().name == GROUP_AMMINISTRATORE \
            else [
            'data_modifica',
            'data_creazione',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'assistito',
            'in_cura_da',
        ]

    def get_exclude(self, request, obj=None):
        lista = []
        if request.user.groups in [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_PAZIENTE]:
            lista.append('assistito')
        if request.user.groups in [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_CAREGIVER]:
            lista.append('in_cura_da')
        return lista

    list_display = ["nome", "sesso", "email", "data_nascita","wallet_address","private_key"]
    ordering = ['nome', 'cognome', 'sesso', 'data_nascita', "wallet_address", "private_key"]
    filter_horizontal = ['in_cura_da', 'groups']

    fieldsets = (
        (
            "Gestione Accessi", {
                "fields": ('password', 'last_login', ('data_modifica', 'data_creazione'),),
            }
        ),
        (
            "Informazione Personali", {
                'fields': ('email', ('nome', 'cognome', 'sesso'),
                           'data_nascita', 'luogo_nascita', 'telefono', 'codice_fiscale',
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito', 'in_cura_da',"wallet_address",'private_key'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')
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
                           ('data_nascita', 'luogo_nascita'), 'codice_fiscale', 'telefono',
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito', 'in_cura_da','wallet_address','private_key'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)
            }
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        """ sovrascrivere form"""
        form = super().get_form(request, obj, **kwargs)
        user_group = request.user.groups.all().first().name
        gruppi = Group.objects.exclude(name=GROUP_AMMINISTRATORE)
        prescrittori = HealthCareUser.objects.filter(
            groups__in=[
                Group.objects.get(name=GROUP_DOTTORE).id,
                Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA).id
            ]
        )
        if obj is None:
            # la terapia non è ancora stata creata => è una CREATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['groups'].choices = [
                                                             (g.id, g) for g in gruppi
                                                         ] + [
                    (Group.objects.get(name=GROUP_AMMINISTRATORE).id,
                     Group.objects.get(name=GROUP_AMMINISTRATORE)),
                ]
                form.base_fields['in_cura_da'].choices = [(p.id, p.show(request=request)) for p in prescrittori]
        else:
            pass
            # la terapia è stata creata => è un UPDATE
            if user_group == GROUP_AMMINISTRATORE:
                form.base_fields['groups'].choices = [
                                                         (g.id, g) for g in gruppi
                                                     ] + [
                                                         (Group.objects.get(name=GROUP_AMMINISTRATORE).id,
                                                          Group.objects.get(name=GROUP_AMMINISTRATORE)),
                                                     ]
                form.base_fields['in_cura_da'].choices = [(p.id, p.show(request=request)) for p in prescrittori]

        return form

    def save_model(self, request, obj, form, change):
        # Verifica se l'utente ha già un portafoglio
        if not obj.wallet_address:
            # Genera un nuovo account se non è presente un portafoglio
            account = Account.create()  # Crea un nuovo account usando la classe Account

            # Stampa il contenuto dell'account

            # Ottieni l'indirizzo del portafoglio generato
            wallet_address = account.address


            # Ottieni la chiave privata dell'account
            private_key = account._private_key.hex()
        else:
            # Usa il wallet esistente
            wallet_address = obj.wallet_address
            private_key = obj.private_key

        # Assegna l'indirizzo generato e la chiave privata al campo wallet_address e private_key
        obj.wallet_address = wallet_address
        obj.private_key = private_key

        # Salva l'oggetto
        super().save_model(request, obj, form, change)

admin.site.register(HealthCareUser, HealthCareUserAdmin)
