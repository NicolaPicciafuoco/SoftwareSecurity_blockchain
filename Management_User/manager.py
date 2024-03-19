from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group

from core.blockchain_utils import create_ethereum_wallet
from core.group_name import *

from django.conf import settings


class HealthCareUserManager(BaseUserManager):

    def create_user(self, email, nome, cognome, sesso, data_nascita, luogo_nascita, indirizzo_residenza, password, **extra_fields):

        user = self.model(
            email=email,
            nome=nome,
            cognome=cognome,
            sesso=sesso,
            data_nascita=data_nascita,
            luogo_nascita=luogo_nascita,
            indirizzo_residenza=indirizzo_residenza,
            is_superuser=False,
            is_staff=True,
            is_active=True,
            **extra_fields
        )

        user.set_password(password)

        wallet_info = create_ethereum_wallet()
        user.ethereum_address = wallet_info['address']
        user.ethereum_private_key = wallet_info['private_key']

        # Stampare le informazioni dell'utente
        if settings.DEBUG:
            print("Nuovo utente creato:", user.email, user.nome, user.cognome, user.sesso, user.data_nascita,
              user.luogo_nascita, user.indirizzo_residenza)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cognome, sesso, data_nascita, luogo_nascita, indirizzo_residenza, password, **extra_fields):
        user = self.model(
            email=email,
            nome=nome,
            cognome=cognome,
            sesso=sesso,
            data_nascita=data_nascita,
            luogo_nascita=luogo_nascita,
            indirizzo_residenza=indirizzo_residenza,
            is_superuser=True,
            is_staff=True,
            is_active=True,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(Group.objects.get_or_create(name=GROUP_AMMINISTRATORE)[0].id)

        wallet_info = create_ethereum_wallet()
        user.ethereum_address = wallet_info['address']
        user.ethereum_private_key = wallet_info['private_key']

        # Stampare le informazioni dell'utente
        if settings.DEBUG:
            print("Nuovo utente creato:", user.email, user.nome, user.cognome, user.sesso, user.data_nascita,
                  user.luogo_nascita, user.indirizzo_residenza)

        user.save(using=self._db)
        return user
