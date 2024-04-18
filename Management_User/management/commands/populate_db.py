import random
from tqdm import tqdm
from django.core.management.base import BaseCommand
from faker import Faker
from Management_User.models import HealthCareUser  # Importa il tuo modello personalizzato
from core.group_name import GROUP_PAZIENTE, GROUP_CAREGIVER, GROUP_DOTTORE, GROUP_DOTTORE_SPECIALISTA, GROUP_AMMINISTRATORE
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from Management_Terapia.models import Terapia
from Management_Prestazioni.models import Prestazione

fake = Faker()

# Imposta la password comune per tutti gli utenti
COMMON_PASSWORD = 'asd123bnm456'


class Command(BaseCommand):
    help = 'Popola il database con utenti di esempio'

    def handle(self, fake=None, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Inizio operazione popolamento db con utenti di esempio'))
        try:
            if not Group.objects.filter(name=GROUP_PAZIENTE).exists():
                g_pazienti = Group.objects.create(name=GROUP_PAZIENTE)
            else:
                g_pazienti = Group.objects.get(name=GROUP_PAZIENTE)

            if not Group.objects.filter(name=GROUP_CAREGIVER).exists():
                g_caregiver = Group.objects.create(name=GROUP_CAREGIVER)
            else:
                g_caregiver = Group.objects.get(name=GROUP_CAREGIVER)

            if not Group.objects.filter(name=GROUP_DOTTORE).exists():
                g_dottore = Group.objects.create(name=GROUP_DOTTORE)
            else:
                g_dottore = Group.objects.get(name=GROUP_DOTTORE)

            if not Group.objects.filter(name=GROUP_DOTTORE_SPECIALISTA).exists():
                g_specialista = Group.objects.create(name=GROUP_DOTTORE_SPECIALISTA)
            else:
                g_specialista = Group.objects.get(name=GROUP_DOTTORE_SPECIALISTA)

            if not Group.objects.filter(name=GROUP_AMMINISTRATORE).exists():
                g_admin = Group.objects.create(name=GROUP_AMMINISTRATORE)
            else:
                g_admin = Group.objects.get(name=GROUP_AMMINISTRATORE)

            self.stdout.write(self.style.SUCCESS('Gruppi creati con successo'))

            # TERAPIA
            content_type_terapia = ContentType.objects.get_for_model(Terapia)
            permission_add_terapia = Permission.objects.get(content_type=content_type_terapia, codename='add_terapia')
            permission_change_terapia = Permission.objects.get(content_type=content_type_terapia, codename='change_terapia')
            permission_delete_terapia = Permission.objects.get(content_type=content_type_terapia, codename='delete_terapia')
            permission_view_terapia = Permission.objects.get(content_type=content_type_terapia, codename='view_terapia')

            # PRESTAZIONE
            content_type_prestazione = ContentType.objects.get_for_model(Prestazione)
            permission_add_prestazione = Permission.objects.get(content_type=content_type_prestazione,
                                                                codename='add_prestazione')
            permission_change_prestazione = Permission.objects.get(content_type=content_type_prestazione,
                                                                   codename='change_prestazione')
            permission_delete_prestazione = Permission.objects.get(content_type=content_type_prestazione,
                                                                   codename='delete_prestazione')
            permission_view_prestazione = Permission.objects.get(content_type=content_type_prestazione,
                                                                 codename='view_prestazione')

            # user
            content_type_utente = ContentType.objects.get_for_model(HealthCareUser)
            permission_view_utente = Permission.objects.get(content_type=content_type_utente,
                                                            codename='view_healthcareuser')
            permission_add_utente = Permission.objects.get(content_type=content_type_utente,
                                                           codename='add_healthcareuser')
            permission_change_utente = Permission.objects.get(content_type=content_type_utente,
                                                              codename='change_healthcareuser')
            permission_delete_utente = Permission.objects.get(content_type=content_type_utente,
                                                              codename='delete_healthcareuser')

            # DOTTORI
            g_dottore.permissions.add(
                permission_add_terapia,
                permission_view_terapia,

                permission_add_prestazione,
                permission_view_prestazione,

                permission_view_utente
            )

            # PAZIENTI
            g_pazienti.permissions.add(
                permission_view_terapia,

                permission_view_prestazione,
                permission_add_prestazione,

                permission_view_utente,
            )

            # CAREGIVER
            g_caregiver.permissions.add(
                permission_view_terapia,

                permission_view_prestazione,
                permission_add_prestazione,

                permission_view_utente
            )

            # DOTTORI SPECIALISTI
            g_specialista.permissions.add(
                permission_add_terapia,
                permission_view_terapia,

                permission_add_prestazione,
                permission_view_prestazione,

                permission_view_utente
            )

            # AMMINISTRATORI
            g_admin.permissions.add(
                permission_view_terapia,
                permission_view_prestazione,
                permission_view_utente,
                permission_add_utente,
                permission_change_utente,
                permission_delete_utente,
            )
            self.stdout.write(self.style.SUCCESS('Permessi creati con successo'))

            num_step_tot = 14 # 13 utenti 1 passo completamento ollegamenti
            with tqdm(total=num_step_tot, desc='Creazione Utenti') as pbar:

                HealthCareUser.objects.create_user(
                    email="admin@admin.it",
                    nome="nome_admin",
                    cognome="cognome_admin",
                    password="admin",
                    sesso=random.choice([HealthCareUser.MALE, HealthCareUser.FEMALE]),
                    data_nascita="1990-01-01",
                    luogo_nascita="Ancona",
                    indirizzo_residenza="Via Primo Maggio 156",
                    wallet_address="",
                    private_key="",
                ).groups.add(g_admin)

                pbar.update(1)

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
                    ).groups.add(g_dottore)
                    pbar.update(1)

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
                    ).groups.add(g_caregiver)
                    pbar.update(1)

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
                    ).groups.add(g_pazienti)
                    pbar.update(1)

                for i in range(3):
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
                    ).groups.add(g_specialista)
                    pbar.update(1)

                # Ottieni i medici

                medici = HealthCareUser.objects.filter(groups=g_dottore)
                medici_sp = HealthCareUser.objects.filter(groups=g_specialista)

                # Ottieni i pazienti
                pazienti = HealthCareUser.objects.filter(groups=g_pazienti)

                # Assegna i pazienti ai medici
                for paziente in pazienti:
                    paziente.in_cura_da.add(random.choice(medici))
                    paziente.in_cura_da.add(random.choice(medici_sp))

                # Ottieni i caregiver
                caregiver = HealthCareUser.objects.filter(groups=g_caregiver)

                # Assegna i pazienti ai caregiver
                for paziente in pazienti:
                    caregiver_person = random.choice(caregiver)
                    caregiver_person.assistito = paziente
                    caregiver_person.save()
                pbar.update(1)
            self.stdout.write(self.style.SUCCESS('Operazione completata con successo'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
