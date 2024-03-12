from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils import http
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import HealthCareUser
from django.contrib.auth.models import Group
from core.group_name import *


class HealthCareUserAdmin(UserAdmin):
    model = HealthCareUser

    def get_queryset(self, request):
        user_group = request.user.groups.all().first()
        all_qs = super(HealthCareUserAdmin, self).get_queryset(request)
        # Group.objects.get(name=GROUP_PAZIENTE)

        if user_group.name == GROUP_AMMINISTRATORE:
            qs = all_qs

        elif user_group.name == GROUP_PAZIENTE:
            qs = all_qs.filter(id=request.user.id, groups=Group.objects.get(name=GROUP_PAZIENTE).id)

        elif user_group.name == GROUP_CAREGIVER:
            qs = all_qs.filter(
                id__in=[request.user.id, request.user.assistito.id if request.user.assistito else None]
            )

        elif user_group.name == GROUP_INFERMIERE:
            qs = all_qs.filter(
                groups__in=[Group.objects.get(name=GROUP_PAZIENTE).id,],
            )

        elif user_group.name == GROUP_DOTTORE:
            qs = all_qs.filter(groups__in=[
                Group.objects.get(name=GROUP_PAZIENTE).id,
                Group.objects.get(name=GROUP_INFERMIERE).id,
                Group.objects.get(name=GROUP_CAREGIVER).id
            ])

        elif user_group.name == GROUP_DOTTORE_SPECIALISTA:
            qs = all_qs.filter(groups=Group.objects.get(name=GROUP_PAZIENTE).id)

        else:
            raise PermissionDenied()
        return qs

    def get_readonly_fields(self, request, obj=None):
        return ['data_modifica', 'data_creazione', 'last_login', ] if request.user.groups.all().first().name == GROUP_AMMINISTRATORE else ['data_modifica', 'data_creazione', 'last_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'assistito',] #'get_assistito']

    list_display = ["nome", "sesso", "email", "data_nascita"]
    ordering = ['nome', 'cognome', 'sesso', 'data_nascita', ]
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito', ), #'get_assistito'),
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
                           'indirizzo_residenza', 'indirizzo_domicilio', 'assistito'),
            }
        ),
        (
            "Permessi", {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)
            }
        ),
    )


admin.site.register(HealthCareUser, HealthCareUserAdmin)
