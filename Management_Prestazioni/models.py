"""ORM delle prestazioni"""
import os
from django.core.exceptions import ValidationError
from Healthcare.settings import MEDIA_ROOT
from Management_User.models import HealthCareUser as User
from django.db import models
from contract.deploy import ContractInteractions
import hashlib
import json
import logging
from django.db import IntegrityError


def upload_to_prestazione(instance, filename):
    """Metodo per aggiornare il path"""
    user_id = str(instance.utente.id) if instance.utente else 'default'

    folder_path = os.path.join(MEDIA_ROOT, 'file_prestazioni', user_id)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    return "file_prestazioni/" + str(user_id) + "/" + filename


class Prestazione(models.Model):
    """Modello Prestazione"""
    file = models.FileField('Referto', upload_to=upload_to_prestazione, null=True, blank=True)
    note = models.TextField('Note', max_length=100, null=True, blank=True)
    utente = models.ForeignKey(User, verbose_name='paziente', related_name='prestazioni_ricevute',
                               on_delete=models.SET_NULL, null=True, blank=False)
    operatore = models.ForeignKey(User, verbose_name='operatore', related_name='prestazioni_fornite',
                                  on_delete=models.SET_NULL, null=True, blank=False)
    hash = models.CharField('hash', max_length=66, null=True, blank=True)


    def filename(self):
        """Metodo per leggere il nome del file"""
        if self.file:
            return os.path.basename(self.file.name)
        return ''

    # Metodo per stampare a schermo le istanze create
    def __str__(self):
        """ritorno della stringa"""
        return f"{self.pk}, {self.filename()}, {self.utente}"

    def clean(self):
        """Sovrascrittura del metodo clean per mostrare errori nella form"""
        super().clean()
        if self.file and self.pk:
            old_instance = Prestazione.objects.get(pk=self.pk)
            if old_instance.file and self.file.name == old_instance.file.name:
                return
        if self.file:
            paziente_id = getattr(self.utente, 'id', None)
            new_file_path = upload_to_prestazione(self, os.path.basename(self.file.name))
            existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'file_prestazioni', str(paziente_id)))
            if os.path.basename(new_file_path) in existing_files:
                raise ValidationError({'file': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})

    def save(self, request=None, *args, **kwargs):
        """ metodo save per il salvataggio"""

        action_type = "Create"

        if self.pk:
            action_type = "Update"
            try:
                old_instance = Prestazione.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except Prestazione.DoesNotExist:
                pass
            if old_instance.utente != self.utente:
                if old_instance.file:
                    old_file_path = old_instance.file.path
                    if os.path.exists(old_file_path):
                        new_path = upload_to_prestazione(self, os.path.basename(self.file.name))
                        os.rename(old_file_path, new_path)
                        self.file.name = os.path.relpath(new_path, MEDIA_ROOT)

        # Part that interacts with the blockchain

        super().save(*args, **kwargs)

        contract_interactions = ContractInteractions()
        address_operatore = self.operatore.wallet_address
        address_paziente = self.utente.wallet_address
        key_operatore = self.operatore.private_key

        hashed_data = self.to_hashed_json()

        self.hash = contract_interactions.log_action(self.id, address_paziente, address_operatore, action_type,
                                                     key_operatore, hashed_data, "Prestazione")
        super().save(*args, **kwargs)
        # Log testing

        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="actions.log", level=logging.INFO)
        logger.info(contract_interactions.get_action_log("Prestazione"))

    def object_to_json_string(self):
        """ metodo per la conversione in json"""
        filtered_object = {
            'id': self.id,
            'utente': self.utente.id,
            'operatore': self.operatore.id,
            'file': self.file.url if self.file else None,
            'note': self.note,
        }
        return json.dumps(filtered_object, sort_keys=True)

    def to_hashed_json(self):
        # Makes a md5 hash of the json object

        json_str = self.object_to_json_string()

        hashed_json = hashlib.md5(json_str.encode()).hexdigest()

        return hashed_json

    def check_json_integrity(self):

        contract_interactions = ContractInteractions()
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="integrity.log", level=logging.INFO)

        # Decrypts the json object and checks if it's been altered
        stored_data = contract_interactions.get_action_by_key(self.id, "Prestazione")
        logger.info("ID: %s", self.id)
        logger.info("Utente: %s", self.utente)
        logger.info("Operatore: %s", self.operatore)
        logger.info("File: %s", self.file)
        logger.info("Note: %s", self.note)
        # Verifica se stored_data non è vuoto prima di accedere all'ultimo elemento
        if stored_data:
            last_tuple = stored_data[-1]  # Ottieni l'ultimo elemento della lista
            last_piece = last_tuple[-1]  # Ottieni l'ultimo elemento di quella tupla

            hashed_json_local = self.to_hashed_json()

            # Stampa le informazioni nel file di log
            logger.info("Stored data: %s", stored_data)
            logger.info("Encrypted JSON local: %s", hashed_json_local)
            logger.info("Last piece: %s", last_piece)

            if last_piece != hashed_json_local:
                raise IntegrityError('Il json è stato alterato')

            return True
        else:
            raise IntegrityError('Nessun dato trovato per questa Prestazione')

    def delete(self, *args, **kwargs):
        ''' metodo per l'eliminazione'''
        contract_interactions = ContractInteractions()
        address_operatore = self.operatore.wallet_address
        address_paziente = self.utente.wallet_address
        key_operatore = self.operatore.private_key
        hashed_data = self.to_hashed_json()

        contract_interactions.log_action(self.id, address_paziente, address_operatore, "Delete", key_operatore, hashed_data,
                                         "Prestazione")
        super().delete(*args, **kwargs)



    class Meta:
        """Definizione dei verbose"""
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'

    def __str__(self):
        """ritorno della stringa"""
        return f"{self.pk}, {self.filename()}, {self.utente}"