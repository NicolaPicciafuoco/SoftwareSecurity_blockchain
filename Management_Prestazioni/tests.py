"""Import"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from Management_User.models import HealthCareUser as User
from Management_Prestazioni.models import Prestazione

class PrestazioneSaveTestCase(TestCase):
    """Classe di test"""
    def setUp(self):
        """Setup delle istanze per i test"""
        self.user = User.objects.create(
            email='test@example.com',
            nome='Test',
            cognome='User',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='TestCity',
            indirizzo_residenza='TestAddress'
        )

        # Simuliamo un file di test
        file_content = b'This is a test file content'
        self.test_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")


    def test_salvataggio_prestazione(self):
        """Testing della funzione di save senza """
        prestazione = Prestazione(
            utente=self.user,
            operatore=self.user,
            note='Test note'
        )

        # Salviamo la Prestazione nel database
        prestazione.save()

        # Verifichiamo che la Prestazione sia stata salvata correttamente
        self.assertIsNotNone(prestazione.id, "La Prestazione non è stata salvata correttamente nel database")

    def test_salvataggio_file_prestazione(self):
        """Testing della funzione di save con il file associato"""
        prestazione = Prestazione.objects.create(
            utente=self.user,
            operatore=self.user,
            file=self.test_file,
            note='Test note'
        )

        # Otteniamo il percorso del file salvato
        file_path = prestazione.file.path

        # Verifichiamo che il file sia stato salvato correttamente
        self.assertTrue(prestazione.file.storage.exists(file_path), "Il file non è stato salvato correttamente")
