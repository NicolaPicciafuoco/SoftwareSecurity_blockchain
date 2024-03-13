""" import"""
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.test import TestCase
from Management_User.models import HealthCareUser as User, HealthCareUser
from .models import Terapia


class TerapiaModelTest(TestCase):
    """ classe dei test per le terapie"""

    def setUp(self):
        """ Creazione utenti di prova"""
        timestamp_suffix = timezone.now().strftime("%Y%m%d%H%M%S")

        # Crea utenti di esempio per i test
        self.paziente = User.objects.create(
            email=f'paziente1_{timestamp_suffix}@example.com',
            nome='NomePaziente',
            cognome='CognomePaziente',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
        )
        self.prescrittore = User.objects.create(
            email=f'prescrittore1_{timestamp_suffix}@example.com',
            nome='NomePrescrittore',
            cognome='CognomePrescrittore',
            sesso=User.FEMALE,
            data_nascita='1990-01-02',
            luogo_nascita='Altro luogo di prova',
            indirizzo_residenza='Altro indirizzo di prova',
        )
        self.utente_testup = User.objects.create(
            email=f'paziente2_{timestamp_suffix}@example.com',
            nome='NomePaziente2',
            cognome='CognomePaziente2',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
        )

    def test_creazione_utente(self):
        """ test per la creazione di un utente"""
        # Crea un utente di esempio
        user = HealthCareUser.objects.create(
            email='test@example.com',
            nome='John',
            cognome='Doe',
            sesso=HealthCareUser.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nome, 'John')
        self.assertEqual(user.cognome, 'Doe')
        self.assertEqual(user.sesso, HealthCareUser.MALE)
        self.assertEqual(str(user.data_nascita), '1990-01-01')
        self.assertEqual(user.luogo_nascita, 'Città di prova')
        self.assertEqual(user.indirizzo_residenza, 'Indirizzo di prova')
        self.assertTrue(user.is_active)

    def test_salvataggio_terapia_con_file(self):
        """ test per il salvataggio di una terapia e di un file associato"""
        utente_test = HealthCareUser.objects.create(
            email='paziente1@example.com',
            nome='NomePaziente',
            cognome='CognomePaziente',
            sesso=HealthCareUser.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
        )

        file_content = b"Contenuto del file di esempio"
        file_name = 'test_file.txt'
        uploaded_file = SimpleUploadedFile(file_name, file_content)

        terapia = Terapia.objects.create(utente=utente_test, prescrittore=utente_test)
        terapia.file = uploaded_file
        terapia.save()

        self.assertTrue(os.path.exists(terapia.file.path))

    def tearDown(self):
        """ rimozione """
        for terapia in Terapia.objects.all():
            if terapia.file:
                os.remove(terapia.file.path)

    def test_modifica_terapia_con_altro_paziente(self):
        """ test upload terapia"""
        terapia = Terapia.objects.create(utente=self.paziente, prescrittore=self.prescrittore)
        terapia.utente = self.utente_testup
        terapia.save()
        self.assertEqual(terapia.utente, self.utente_testup)
        self.assertEqual(terapia.prescrittore, self.prescrittore)
