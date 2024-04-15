from django.apps import AppConfig
from core.group_name import *


class ManagementUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Management_User'
    verbose_name = 'gestione utenti'

    # def ready(self):
    #     try:
    #         from django.contrib.auth.models import Group
    #         paziente, created_paziente = Group.objects.get_or_create(name=GROUP_PAZIENTE)
    #         caregiver, created_caregiver = Group.objects.get_or_create(name=GROUP_CAREGIVER)
    #         dottore, created_dottore = Group.objects.get_or_create(name=GROUP_DOTTORE)
    #         dottore_specialista, created_dottore_specialista = Group.objects.get_or_create(name=GROUP_DOTTORE_SPECIALISTA)
    #         amministratore, created_amministratore = Group.objects.get_or_create(name=GROUP_AMMINISTRATORE)
    #     except Exception as e:
    #         return
