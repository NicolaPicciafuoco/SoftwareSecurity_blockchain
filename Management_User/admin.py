from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import HealthCareUser


class HealthCareUserAdmin(UserAdmin):
    model = HealthCareUser

    def get_queryset(self, request):
        qs = super(HealthCareUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)

    list_display = ["nome", "email", "data_nascita"]
    ordering = ['nome', 'cognome', 'sesso', 'data_nascita', ]
    # exclude = ['username']
    readonly_fields = ['data_modifica', 'data_creazione', 'last_login']
    # username first_name last_name
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'caregiver'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')  # , 'user_permissions')
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'caregiver'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)
            }
        ),
    )


admin.site.register(HealthCareUser, HealthCareUserAdmin)
