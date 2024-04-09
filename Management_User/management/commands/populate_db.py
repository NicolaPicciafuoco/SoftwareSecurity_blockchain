import random

from django.core.management.base import BaseCommand
from faker import Faker
from Management_User.models import HealthCareUser  # Importa il tuo modello personalizzato

fake = Faker()

# Imposta la password comune per tutti gli utenti
COMMON_PASSWORD = 'asd123bnm456'


class Command(BaseCommand):
    help = 'Popola il database con utenti di esempio'

    def handle(self, fake=None, *args, **kwargs):
        # Crea due dottori
        for i in range(2):
            nome_dottore = f'NOME_dottore_{i}'
            HealthCareUser.objects.create_user(
                email=f'EMAIL_dottore_{i}@dottore{i}.it',
                nome=nome_dottore,
                cognome='',
                password=COMMON_PASSWORD,
                sesso=random.choice([HealthCareUser.MALE, HealthCareUser.FEMALE]),
                data_nascita="1990-01-01",
                luogo_nascita="Ancona",
                indirizzo_residenza="Via Primo Maggio 156",
                wallet_address="",
                private_key="",
                # is_staff=True
            ).groups.add(3)

        # Crea due caregiver
        for i in range(2):
            nome_caregiver = f'nome_caregiver_{i}'
            caregiver = HealthCareUser.objects.create_user(
                email=f'EMAIL_caregiver_{i}@caregiver{i}.it',
                nome=nome_caregiver,
                cognome='',
                password=COMMON_PASSWORD,
                sesso=random.choice([HealthCareUser.MALE, HealthCareUser.FEMALE]),
                data_nascita="1990-01-01",
                luogo_nascita="Ancona",
                indirizzo_residenza="Via Primo Maggio 156",
                wallet_address="",
                private_key="",
                # is_staff=True
            ).groups.add(2)  # definito un gruppo per i caregiver

        # Crea tre pazienti
        for i in range(5):  # Modifica la linea interessata
            HealthCareUser.objects.create_user(
                email=f'EMAIL_paziente_{i}@paziente{i}.it',
                nome=f'NOME_paziente_{i}',
                cognome="",
                password=COMMON_PASSWORD,
                sesso=random.choice([HealthCareUser.MALE, HealthCareUser.FEMALE]),
                data_nascita="1990-01-01",
                luogo_nascita="Ancona",
                indirizzo_residenza="Via Primo Maggio 156",
                wallet_address="",
                private_key="",
                # is_staff=True
            ).groups.add(1)

        for i in range(3):
            # Crea un dottore specialista
            HealthCareUser.objects.create_user(
                email=f'EMAIL_dottore_specialista{i}@dottorespecialista{i}.it',
                nome=f'NOME_dottore_specialista{i}',
                cognome="",
                password=COMMON_PASSWORD,
                sesso=random.choice([HealthCareUser.MALE, HealthCareUser.FEMALE]),
                data_nascita="1990-01-01",
                luogo_nascita="Ancona",
                indirizzo_residenza="Via Primo Maggio 156",
                wallet_address="",
                private_key="",
                # is_staff=True
            ).groups.add(4)
        # Ottieni i medici
        medici_group = Group.objects.get(id=3)
        medici = HealthCareUser.objects.filter(groups=medici_group)

        # Ottieni i pazienti
        pazienti_group = Group.objects.get(id=1)
        pazienti = HealthCareUser.objects.filter(groups=pazienti_group)

        # Assegna i pazienti ai medici
        for paziente in pazienti:
            medico = random.choice(medici)
            paziente.in_cura_da.add(medico)

        # Ottieni i caregiver
        caregiver_group = Group.objects.get(id=2)
        caregiver = HealthCareUser.objects.filter(groups=caregiver_group)

        # Assegna i pazienti ai caregiver
        for paziente in pazienti:
            caregiver_person = random.choice(caregiver)
            paziente.assistito = caregiver_person
            paziente.save()

        self.stdout.write(self.style.SUCCESS('Utenti creati con successo'))


# PERMESSI
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from Management_Terapia.models import Terapia
from Management_Prestazioni.models import Prestazione

# Assegna i permessi ai dottori
dottori_group = Group.objects.get(id=3)
pazienti_group = Group.objects.get(id=1)
caregiver_group = Group.objects.get(id=2)
dottori_specialisti_group = Group.objects.get(id=4)

# TERAPIA
content_type_terapia = ContentType.objects.get_for_model(Terapia)
permission_add_terapia = Permission.objects.get(content_type=content_type_terapia, codename='add_terapia')
permission_change_terapia = Permission.objects.get(content_type=content_type_terapia, codename='change_terapia')
permission_delete_terapia = Permission.objects.get(content_type=content_type_terapia, codename='delete_terapia')
permission_view_terapia = Permission.objects.get(content_type=content_type_terapia, codename='view_terapia')

# PRESTAZIONE
content_type_prestazione = ContentType.objects.get_for_model(Prestazione)
permission_add_prestazione = Permission.objects.get(content_type=content_type_prestazione, codename='add_prestazione')
permission_change_prestazione = Permission.objects.get(content_type=content_type_prestazione, codename='change_prestazione')
permission_delete_prestazione = Permission.objects.get(content_type=content_type_prestazione, codename='delete_prestazione')
permission_view_prestazione = Permission.objects.get(content_type=content_type_prestazione, codename='view_prestazione')

# user
content_type_utente = ContentType.objects.get_for_model(HealthCareUser)
permission_view_utente = Permission.objects.get(content_type=content_type_utente, codename='view_healthcareuser')



#DOTTORI
dottori_group.permissions.add(
    permission_add_terapia,permission_change_terapia,permission_delete_terapia,permission_view_terapia,
    permission_add_prestazione,permission_change_prestazione,permission_delete_prestazione,permission_view_prestazione
)

#PAZIENTI
pazienti_group.permissions.add(permission_view_terapia,permission_view_prestazione,permission_view_utente)

#CAREGIVER
caregiver_group.permissions.add(permission_view_terapia,permission_view_prestazione,permission_add_prestazione,permission_change_prestazione,permission_delete_prestazione)

#DOTTORI SPECIALISTI
dottori_specialisti_group.permissions.add(
    permission_add_terapia,permission_change_terapia,permission_delete_terapia,permission_view_terapia,
    permission_add_prestazione,permission_change_prestazione,permission_delete_prestazione,permission_view_prestazione
)
