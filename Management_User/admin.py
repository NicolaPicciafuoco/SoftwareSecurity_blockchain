from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.group_get_queryset import return_queryset_user
from .models import HealthCareUser
from core.group_name import *


class HealthCareUserAdmin(UserAdmin):
    model = HealthCareUser

    def get_queryset(self, request):
        return return_queryset_user(self, request, HealthCareUserAdmin)

    def get_readonly_fields(self, request, obj=None):
        return ['data_modifica', 'data_creazione', 'last_login', ] if request.user.groups.all().first().name == GROUP_AMMINISTRATORE else ['data_modifica', 'data_creazione', 'last_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'assistito', 'in_cura_da']

    list_display = ["nome", "sesso", "email", "data_nascita"]
    ordering = ['nome', 'cognome', 'sesso', 'data_nascita', ]
    filter_horizontal = ['in_cura_da', 'groups']
    # exclude = ['username']
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito', 'in_cura_da'),
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito', 'in_cura_da'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)
            }
        ),
    )


admin.site.register(HealthCareUser, HealthCareUserAdmin)
