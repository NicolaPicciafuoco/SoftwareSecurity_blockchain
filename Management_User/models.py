from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission, Group
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from .manager import HealthCareUserManager
from core.group_name import (GROUP_DOTTORE,
                             GROUP_DOTTORE_SPECIALISTA,
                             GROUP_AMMINISTRATORE,
                             GROUP_PAZIENTE)


class HealthCareUser(AbstractBaseUser, PermissionsMixin):
    """
         Modello tel med user cioè del utente del sistema
    """
    MALE = 1
    FEMALE = 2

    SESSO_SCELTE = [
        (MALE,   'Maschio'),
        (FEMALE, 'Femmina'),
    ]
    telefono_validator = RegexValidator(
        regex=r'^[\d\s-]+$',
        message='Telefono number can only contain digits, dashes, and spaces.',
        code='invalid_telefono'
    )
    codice_fiscale_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]+$',
        message='Codice fiscale can only contain alphanumeric characters.',
        code='invalid_codice_fiscale'
    )
    indirizzo_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9\s]+$',
        message='Indirizzo can only contain alphanumeric characters and spaces.',
        code='invalid_indirizzo'
    )
    email = models.EmailField(
        'indirizzo e-mail',
        unique=True,
        error_messages={'unique': 'Questa e-mail è già in uso'}
    )
    nome = models.CharField('Nome', max_length=150)
    cognome = models.CharField('Cognome', max_length=150, null=True, blank=True)
    sesso = models.SmallIntegerField(choices=SESSO_SCELTE, default=MALE)
    data_nascita = models.DateField('Data di nascita')

    luogo_nascita = models.CharField('Luogo nascita', max_length=200, null=True, blank=True)

    telefono = models.CharField(
        'Numero di telefono',
        max_length=14, null=True, blank=True,
        validators=[telefono_validator]
    )

    codice_fiscale = models.CharField(
        'Codice fiscale',
        max_length=16, null=True, blank=True,
        validators=[codice_fiscale_validator]
    )

    indirizzo_residenza = models.CharField(
        'Indirizzo  di residenza',
        max_length=255, null=True, blank=True,
        validators=[indirizzo_validator]
    )

    indirizzo_domicilio = models.CharField(
        'Indirizzo di domicilio',
        max_length=255, null=True, blank=True,
        validators=[indirizzo_validator]
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        related_name='telmed_user_permissions',
        blank=True
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        related_name='telmed_user_groups',
        blank=True
    )

    assistito = models.ForeignKey(
        'self',
        verbose_name='Assistito',
        related_name='caregiver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    in_cura_da = models.ManyToManyField(
        'self',
        verbose_name='In cura da',
        related_name='pazienti_assegnati',
        blank=True,

    )

    is_staff = models.BooleanField(
        "Staff",
        default=True,
    )
    is_active = models.BooleanField(
        "attivo",
        default=True,
    )
    data_creazione = models.DateTimeField(
        'Data di creazione',
        auto_now_add=True,
        editable=False,
    )
    data_modifica = models.DateTimeField(
        'Data di aggiornamento',
        auto_now=True,
        editable=False,
    )

    objects = HealthCareUserManager()

    USERNAME_FIELD = 'email'

    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = [
        'nome', 'cognome', 'sesso', 'data_nascita', 'luogo_nascita', 'indirizzo_residenza'
    ]

    def get_sesso(self):
        if self.groups.first() == GROUP_PAZIENTE:
            return f" {self.SESSO_SCELTE[0][1]:>8}" if self.sesso == 1 else f" {self.SESSO_SCELTE[1][1]:>8}"
        return ""

    def __str__(self):
        return f"{self.nome} {self.cognome if self.cognome else ''}{self.get_sesso()}{
        ' ' if self.groups.first() is not None else ''}{
        self.groups.first() if self.groups.first() is not None else ''}"

    def clean(self):
        try:
            if self.groups and self.groups.count() > 1:
                raise ValidationError({'groups': ['Selezionare un gruppo per utente.']})
        except Exception:
            pass
        super().clean()

    def show(self, request):
        lista_check = [GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_AMMINISTRATORE]
        if request.user.groups.first().name in lista_check:
            return f"{self.__str__()} {self.data_nascita if self.groups.first().name == GROUP_PAZIENTE else ''}"
        return self.__str__()

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
        ordering = ['nome', 'cognome', 'sesso', 'data_nascita',]
