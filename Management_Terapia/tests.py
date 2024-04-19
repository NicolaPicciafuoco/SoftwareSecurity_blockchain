from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Management_Terapia.models import Terapia
from Management_User.models import HealthCareUser as User
from django.db.models import Max

class TerapiaTestCase(TestCase):


    def setUp(self):
        # Elimina tutte le istanze di Terapia prima di ogni test
        Terapia.objects.all().delete()

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

        self.prescrittore = User.objects.create(
            email='user3@example.com',
            nome='UserProvaprescrittore',
            cognome='CognomeProvaprescrittore',
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
        # Creare una nuova istanza di Terapia
        Terapia.objects.create(
            utente=self.user,
            prescrittore=self.prescrittore,
            file=self.file if self.file else None,
            note='Nota di prova'
        )

        self.assertTrue(Terapia.objects.exists())

    def test_update_function(self):
        # Creare una nuova istanza di Terapia
        terapia = Terapia.objects.create(
            utente=self.user,
            prescrittore=self.prescrittore,
            file=self.file if self.file else None,
            note='Nota di prova2'
        )

        # Modifica dei dati dell'istanza di Terapia
        new_note = "Nuova nota di prova"
        terapia.note = new_note
        terapia.save()

        # Verifica che l'istanza di Terapia sia stata aggiornata correttamente nel database
        updated_terapia = Terapia.objects.get(pk=terapia.pk)
        self.assertEqual(updated_terapia.note, new_note)

    def test_delete_function(self):
        # Creare una nuova istanza di Terapia
        Terapia.objects.create(
            utente=self.user,
            prescrittore=self.prescrittore,
            file=self.file if self.file else None,
            note='Nota di prova'
        )
        # Eliminare l'istanza di Terapia
        Terapia.objects.all().delete()
        # Verifico che Terapia.objects.all().delete() abbia eliminato tutto
        self.assertFalse(Terapia.objects.exists())



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



