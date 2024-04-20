from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Management_Prestazioni.models import Prestazione
from Management_User.models import HealthCareUser as User


class PrestazioneTestCase(TestCase):

    def setUp(self):
        # Elimina tutte le istanze di Prestazione prima di ogni test
        Prestazione.objects.all().delete()
        # Creazione degli utenti di test
        self.user = User.objects.create(
            email='user@example.com',
            nome='UserProva',
            cognome='CognomeProva',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
            wallet_address='0x9F74Ae796089913245c9e41D408E8c29B784eB67',
            private_key='0xd9f5dabf3c2e2395887f39091b1408447148626dbc52eb6a8ddcf23a31118cea',
        )

        self.operatore = User.objects.create(
            email='user3@example.com',
            nome='UserProvaoperatore',
            cognome='CognomeProvaoperatore',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
            wallet_address='0x9F74Ae796089913245c9e41D408E8c29B784eB67',
            private_key='0xd9f5dabf3c2e2395887f39091b1408447148626dbc52eb6a8ddcf23a31118cea',
        )

        # Definizione di un file di test
        file_content = b"Contenuto del file di esempio"
        self.file = SimpleUploadedFile("test_file.txt", file_content)

    def test_save_function(self):
        # Creare una nuova istanza di Prestazione
        Prestazione.objects.create(
            utente=self.user,
            operatore=self.operatore,
            file=self.file if self.file else None,
            note='Nota di prova'
        )

        self.assertTrue(Prestazione.objects.exists())

    def test_update_function(self):
        # Creare una nuova istanza di Prestazione
        prestazione = Prestazione.objects.create(
            utente=self.user,
            operatore=self.operatore,
            file=self.file if self.file else None,
            note='Nota di prova2'
        )

        # Modifica dei dati dell'istanza di Prestazione
        new_note = "Nuova nota di prova"
        prestazione.note = new_note
        prestazione.save()

        # Verifica che l'istanza di Prestazione sia stata aggiornata correttamente nel database
        updated_prestazione = Prestazione.objects.get(pk=prestazione.pk)
        self.assertEqual(updated_prestazione.note, new_note)

    def test_delete_function(self):
        # Creare una nuova istanza di Prestazione
        Prestazione.objects.create(
            utente=self.user,
            operatore=self.operatore,
            file=self.file if self.file else None,
            note='Nota di prova'
        )
        # Eliminare l'istanza di Prestazione
        Prestazione.objects.all().delete()
        # Verifico che Prestazione.objects.all().delete() abbia eliminato tutto
        self.assertFalse(Prestazione.objects.exists())

    def test_creazione_utente(self):
        # Creazione di un nuovo utente
        user = User.objects.create(
            email='useruseruser@example.com',
            nome='NomeUtente',
            cognome='CognomeUtente',
            sesso=User.MALE,
            data_nascita='1990-01-01',
            luogo_nascita='Città di prova',
            indirizzo_residenza='Indirizzo di prova',
            wallet_address='0x9F74Ae796089913245c9e41D408E8c29B784eB67',
            private_key='0xd9f5dabf3c2e2395887f39091b1408447148626dbc52eb6a8ddcf23a31118cea',
        )

        # Verifica che l'utente sia stato creato correttamente
        self.assertTrue(User.objects.filter(pk=user.pk).exists())
