"""File di specifica del Manager per l'utente custom"""
from web3 import Account
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from core.group_name import GROUP_AMMINISTRATORE


class HealthCareUserManager(BaseUserManager):
    """Manager per l'utente custom"""
    def create_user(self, email, nome, cognome, sesso,
                    data_nascita, luogo_nascita, indirizzo_residenza,
                    password, **extra_fields):
        """crea un utente"""
        account = Account.create()
        wallet_address_local = account.address
        private_key_local = account._private_key.hex()
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
            wallet_address=wallet_address_local,
            private_key=private_key_local,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def add_user_to_admin_group(self, user):
        """aggiunge un utente admin group"""
        admin_group, _ = Group.objects.get_or_create(name=GROUP_AMMINISTRATORE)
        user.groups.add(admin_group)
        user.save()

    def create_superuser(self, email, nome, cognome, sesso,
                         data_nascita, luogo_nascita,
                         indirizzo_residenza, password,
                         **extra_fields):
        """crea un superuser"""
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
        user.save(using=self._db)
        user.groups.add(
            Group.objects.get_or_create(name=GROUP_AMMINISTRATORE)[0].id
        )
        user.save(using=self._db)
        return user
