from django.apps import AppConfig
from core.group_name import *


class ManagementUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Management_User'
    verbose_name = 'gestione utenti'
