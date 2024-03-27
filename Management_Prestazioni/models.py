"""ORM delle prestazioni"""
import os
from django.core.exceptions import ValidationError
from Healthcare.settings import MEDIA_ROOT
from Management_User.models import HealthCareUser as User
from django.db import models
from web3 import Web3
from web3 import Account


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

    def deploy_contract(self):
        # Collegamento al nodo Ethereum Besu
        w3 = Web3(Web3.HTTPProvider('http://rpcnode:8545'))

        # Carica il bytecode del contratto Solidity
        with open('contract_bytecode.txt', 'r') as file:
            contract_bytecode = file.read().replace('\n', '')

        # Deploy del contratto sulla rete Besu
        contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        tx_hash = contract.constructor().transact({'from': 'your_account_address', 'gas': 5000000})

        # Attendere il completamento della transazione di deploy
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        # Ottenere l'indirizzo del contratto deployato
        contract_address = tx_receipt.contractAddress

        # Salva l'indirizzo del contratto nell'istanza di Prestazione
        self.contract_address = contract_address
        self.save()

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
        """Metodo per la gestione degli input della form"""
        super().clean()

        if self.file and self.utente:
            paziente_id = getattr(self.utente, 'id', None)
            if paziente_id is not None:
                new_file_path = upload_to_prestazione(self, os.path.basename(self.file.name))
                existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'file_prestazioni', str(paziente_id)))

                if os.path.basename(new_file_path) in existing_files:
                    raise ValidationError({'file': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})
            else:
                raise ValidationError({'utente': ['L\'utente associato non è valido.']})

    def save(self, request=None, *args, **kwargs):
        """Metodo per salvare il file nel path personalizzato per utente"""
        if self.pk:
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

        super().save(*args, **kwargs)

    class Meta:
        """Definizione dei verbose"""
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'
