from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
# Create your tests here.
from django.test import TestCase
from Management_User.models import HealthCareUser as User, HealthCareUser
from .models import Terapia, get_upload_path
from django.core.exceptions import ValidationError
import os



class TerapiaModelTest(TestCase):
    def setUp(self):
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

        # Verifica che l'utente sia stato creato correttamente
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.nome, 'John')
        self.assertEqual(user.cognome, 'Doe')
        self.assertEqual(user.sesso, HealthCareUser.MALE)
        self.assertEqual(str(user.data_nascita), '1990-01-01')
        self.assertEqual(user.luogo_nascita, 'Città di prova')
        self.assertEqual(user.indirizzo_residenza, 'Indirizzo di prova')

        # Verifica che l'utente sia attivo
        self.assertTrue(user.is_active)

    # def test_validazione_nome_file_univoco(self):
    #     # Crea una terapia di esempio
    #     terapia = Terapia.objects.create(utente=self.paziente, prescrittore=self.prescrittore, note='Note di test')
    #
    #     # Tentativo di creare un'altra terapia con gli stessi utente e prescrittore
    #     with self.assertRaises(ValidationError):
    #         Terapia.objects.create(utente=self.paziente, prescrittore=self.prescrittore, note='Altre note')

    def test_salvataggio_terapia_con_file(self):
        # Crea un utente di esempio per il test
        utente_test = HealthCareUser.objects.create(
            email='paziente1@example.com',
            nome='NomePaziente',
            cognome='CognomePaziente',
            sesso=HealthCareUser.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
        )

        # Crea un file di esempio (puoi personalizzare il contenuto e il nome del file)
        file_content = b"Contenuto del file di esempio"
        file_name = 'test_file.txt'
        uploaded_file = SimpleUploadedFile(file_name, file_content)

        # Crea la terapia e assegna il file
        terapia = Terapia.objects.create(utente=utente_test, prescrittore=utente_test)
        terapia.file = uploaded_file
        terapia.save()

        # Verifica che il file sia stato salvato correttamente
        self.assertTrue(os.path.exists(terapia.file.path))
    #
    #     # Crea la terapia associandola all'utente e al file
    #     terapia = Terapia.objects.create(utente=self.utente_test, prescrittore=self.utente_test, file=uploaded_file)
    #     terapia.save()
    #
    #     self.assertTrue(os.path.exists(terapia.file.path))

    # def test_validazione_nome_file_univoco(self):
    #     # Crea una terapia di esempio con un file
    #     file_content = b"Contenuto del file di esempio"
    #     file_name = 'test_file.txt'
    #     uploaded_file = SimpleUploadedFile(file_name, file_content)
    #     terapia1 = Terapia.objects.create(utente=self.paziente, prescrittore=self.prescrittore, file=uploaded_file)
    #
    #     # Assicurati che la terapia1 sia salvata correttamente
    #     self.assertIsNotNone(terapia1.id)
    #
    #     # Crea una seconda terapia con lo stesso utente, prescrittore e file
    #     try:
    #         terapia2 = Terapia.objects.create(utente=self.paziente, prescrittore=self.prescrittore, file=uploaded_file)
    #     except ValidationError as e:
    #         # Stampa il messaggio di validazione effettivo
    #         print("Validation Error Message:", e.message_dict.get('file', None))
    #     else:
    #         # Se non solleva un'eccezione di validazione, segnala il fallimento del test
    #         self.fail("ValidationError non sollevata")
    #
    #     # Assicurati che la terapia2 non sia stata salvata
    #     self.assertIsNone(terapia2.id)
    #
    #     # Assicurati che il messaggio di validazione contenga il testo desiderato
    #     self.assertIn('Il file con lo stesso nome esiste già. Scegli un nome diverso.',
    #                   e.message_dict.get('file', None))
    #
    #     # Stampa alcuni dettagli utili per il debug
    #     print("Terapia1 ID:", terapia1.id)
    #     print("Terapia2 ID:", terapia2.id)
    #
    #     # Stampa i nomi dei file
    #     print("Terapia1 File Name:", terapia1.file.name)
    #     print("Terapia2 File Name:", terapia2.file.name)