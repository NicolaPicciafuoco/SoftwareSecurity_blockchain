import web3
from django.core.exceptions import ValidationError
from Management_User.models import HealthCareUser as User
from Healthcare.settings import MEDIA_ROOT
from django.db import models
from dotenv import load_dotenv
from cryptography import fernet
import json
import base64
import logging
import os

from contract.deploy import ContractInteractions


def get_upload_path(instance, filename):
    """ funzione per impostare il path"""
    user_id = str(instance.utente.id) if instance.utente else 'default'

    folder_path = os.path.join(MEDIA_ROOT, 'file_terapie', user_id)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    return "file_terapie/" + str(user_id) + "/" + filename


class Terapia(models.Model):
    ''' Crea il modello sulla tabella di terapia'''
    utente = models.ForeignKey(User, verbose_name='paziente', related_name='terapie',
                               on_delete=models.SET_NULL, default=None, null=True, blank=True)
    prescrittore = models.ForeignKey(User, verbose_name='prescrittore', related_name='terapie_prescritte',
                                     on_delete=models.SET_NULL, default=None, null=True, blank=True)
    file = models.FileField('Terapia', upload_to=get_upload_path, null=True, blank=True)
    note = models.CharField('note', max_length=100, null=True, blank=True)
    hash = models.CharField('hash', max_length=66, null=True, blank=True)

    def clean(self):
        """Sovrascrittura del metodo clean per mostrare errori nella form"""
        super().clean()
        if self.file and self.pk:
            old_instance = Terapia.objects.get(pk=self.pk)
            if old_instance.file and self.file.name == old_instance.file.name:
                return
        if self.file:
            paziente_id = getattr(self.utente, 'id', None)
            new_file_path = get_upload_path(self, os.path.basename(self.file.name))
            existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'file_terapie', str(paziente_id)))
            if os.path.basename(new_file_path) in existing_files:
                raise ValidationError({'file': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})

    def save(self, request=None, *args, **kwargs):
        """ metodo save per il salvataggio"""

        action_type = "Create"

        if self.pk:
            action_type = "Update"
            try:
                old_instance = Terapia.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except Terapia.DoesNotExist:
                pass
            if old_instance.utente != self.utente:
                if old_instance.file:
                    old_file_path = old_instance.file.path
                    if os.path.exists(old_file_path):
                        new_path = get_upload_path(self, os.path.basename(self.file.name))
                        os.rename(old_file_path, new_path)
                        self.file.name = os.path.relpath(new_path, MEDIA_ROOT)

        # Part that interacts with the blockchain

        super().save(*args, **kwargs)

        contract_interactions = ContractInteractions()
        address_medico = self.prescrittore.wallet_address
        address_paziente = self.utente.wallet_address
        key_medico = self.prescrittore.private_key

        # Encrypts the json object

        encrypted_data = self.to_encrypted_json()

        # Checks if the data has been altered

        ''' Commentato finché non decidiamo come gestire la faccenda dell'integrità dei dati

        stored_data = contract_interactions.get_action_by_key(self.id, "Terapia")[4]



        if not stored_data:
            self.check_json_integrity(stored_data)

        '''

        self.hash = contract_interactions.log_action(self.id, address_paziente, address_medico, action_type,
                                                        key_medico, encrypted_data, "Terapia")

        # Log testing

        logger = logging.getLogger(__name__)
        logging.basicConfig(filename="actions.log", level=logging.INFO)
        logger.info(contract_interactions.get_action_log("Terapia"))



    def object_to_json(self):
        """ metodo per la conversione in json"""
        filtered_object = {
            'id': self.id,
            'utente': self.utente.id,
            'prescrittore': self.prescrittore.id,
            'file': self.file.url if self.file else None,
            'note': self.note,
        }
        return json.dumps(filtered_object)

    def to_encrypted_json(self):
        # Encrypts the json object

        json_object = self.object_to_json()

        load_dotenv()

        key = os.getenv('FERNET_KEY')

        encrypted_json = fernet.Fernet(key).encrypt(json_object.encode())

        return encrypted_json

    def check_json_integrity(self, encrypted_json):
        # Decrypts the json object and checks if it's been altered

        json_object = self.object_to_json()

        load_dotenv()

        key = os.getenv('FERNET_KEY')

        decrypted_json = fernet.Fernet(key).decrypt(encrypted_json).decode()

        if json_object != decrypted_json:
            raise ValidationError('Il json è stato alterato')

        return True
    # def check_json_integrity_nicola(self):
    #     contract_interactions = ContractInteractions()
    #
    #     # Decrypts the json object and checks if it's been altered
    #     stored_data = contract_interactions.get_action_by_key(self.id, "Terapia")
    #     encrypted_json_local = self.to_encrypted_json()
    #     encrypted_json = stored_data[-1]
    #
    #     if encrypted_json != encrypted_json_local:
    #         raise ValidationError('Il json è stato alterato')
    #
    #     return True

    def __str__(self):
        ''' il ritorno della stringa'''
        return f"Terapia {self.pk}: {self.note}"

    class Meta:
        ''' per il nome plurale'''
        verbose_name_plural = "Terapie"
