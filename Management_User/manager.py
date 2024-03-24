from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from core.group_name import *
from web3 import Web3


class HealthCareUserManager(BaseUserManager):

        def create_user(self, email, nome, cognome, sesso, data_nascita, luogo_nascita, indirizzo_residenza, password,
                        wallet_address=None,private_key=None, **extra_fields):
            user = self.model(
                email=self.normalize_email(email),
                nome=nome,
                cognome=cognome,
                sesso=sesso,
                data_nascita=data_nascita,
                luogo_nascita=luogo_nascita,
                indirizzo_residenza=indirizzo_residenza,
                is_superuser=False,
                is_staff=True,
                is_active=True,
                wallet_address="ciao",  # Assegna sempre "ciao" come valore predefinito
                private_key="ciao",
                **extra_fields
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, nome, cognome, sesso, data_nascita, luogo_nascita, indirizzo_residenza, password,
                         **extra_fields):
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
            **extra_fields
        )

        user.set_password(password)
        user.groups.add(Group.objects.get_or_create(name=GROUP_AMMINISTRATORE)[0].id)
        user.save(using=self._db)
        return user
