from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from Management_User.models import HealthCareUser as User
from Healthcare.settings import MEDIA_ROOT
from django.db import models
import hashlib
import json
import os
from django.db import IntegrityError
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
    file = models.FileField('Terapia', upload_to=get_upload_path, null=True, blank=True)
    note = models.TextField('note', max_length=100, null=True, blank=True,
                            validators=[RegexValidator(regex=r'^[a-zA-Z0-9\s]*$',
                                                       message='solo lettere, numeri e spazzi sono consentiti')])
    utente = models.ForeignKey(User, verbose_name='paziente', related_name='terapie',
                               on_delete=models.SET_NULL, default=None, null=True, blank=True)
    prescrittore = models.ForeignKey(User, verbose_name='prescrittore', related_name='terapie_prescritte',
                                     on_delete=models.SET_NULL, default=None, null=True, blank=True)
    hash = models.CharField('hash', max_length=66, null=True, blank=True)

    def clean(self):
        """Sovrascrittura del metodo clean per mostrare errori nella form"""
        super().clean()
        max_size = 2 * 1024 * 1024  # 2 megabyte in byte
        if self.file and self.pk:
            old_instance = Terapia.objects.get(pk=self.pk)
            if old_instance.file and self.file.name == old_instance.file.name:
                return
        if self.file:
            if isinstance(self.file.size, int):
                dim_file = self.file.size
                if dim_file > max_size:
                    raise ValidationError('Il file è troppo grande. La dimensione massima consentita è 2 MB.')
            else:
                raise ValidationError('La dimensione del file non è un valore numerico valido.')
            allowed_extensions = ['.pdf', '.doc', '.docx','.png','.jpeg']  # Estensioni consentite
            ext = os.path.splitext(self.file.name)[1]  # Ottieni l'estensione del file
            if ext.lower() not in allowed_extensions:
                raise ValidationError(
                    'Il tipo di file non è supportato. Si prega di caricare un file con estensione .pdf, .doc, .docx., pgn, jpeg')
            paziente_id = getattr(self.utente, 'id', None)
            new_file_path = get_upload_path(self, os.path.basename(self.file.name))
            existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'file_terapie', str(paziente_id)))
            if os.path.basename(new_file_path) in existing_files:
                raise ValidationError({'file': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})

    def save(self, request=None, *args, **kwargs):
        """ metodo save per il salvataggio"""

        action_type = "Create"
        old_instance = None

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

        hashed_data = self.to_hashed_json()

        self.hash = contract_interactions.log_action(self.id, address_paziente, address_medico, action_type,
                                                     key_medico, hashed_data, "Terapia")
        # salvami solo la il campo hash
        super().save(update_fields=['hash'])

    def object_to_json_string(self):
        """ metodo per la conversione in json"""
        filtered_object = {
            'id': self.id,
            'utente': self.utente.id,
            'prescrittore': self.prescrittore.id,
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

        # Decrypts the json object and checks if it's been altered
        stored_data = contract_interactions.get_action_by_key(self.id, "Terapia")

        # Verifica se stored_data non è vuoto prima di accedere all'ultimo elemento
        if stored_data:
            last_tuple = stored_data[-1]  # Ottieni l'ultimo elemento della lista
            last_piece = last_tuple[-1]  # Ottieni l'ultimo elemento di quella tupla

            hashed_json_local = self.to_hashed_json()

            if last_piece != hashed_json_local:
                raise IntegrityError('Il json è stato alterato')

            return True
        else:
            raise IntegrityError('Integrità compromessa')

    def delete(self, *args, **kwargs):
        ''' metodo per l'eliminazione'''
        contract_interactions = ContractInteractions()
        address_medico = self.prescrittore.wallet_address
        address_paziente = self.utente.wallet_address
        key_medico = self.prescrittore.private_key
        hashed_data = self.to_hashed_json()

        contract_interactions.log_action(self.id, address_paziente, address_medico, "Delete", key_medico, hashed_data,
                                         "Terapia")
        super().delete(*args, **kwargs)

    def __str__(self):
        ''' Il ritorno della stringa'''
        return f"Terapia {self.prescrittore} -> {self.utente} hash[{str(self.hash)[:10] if self.hash else None}...]"

    class Meta:
        ''' per il nome plurale'''
        verbose_name_plural = "Terapie"
