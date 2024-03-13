"""ORM delle prestazioni"""
import os
from django.core.exceptions import ValidationError
from Healthcare.settings import MEDIA_ROOT
from Management_User.models import HealthCareUser as User
from django.db import models


def upload_to_prestazione(instance, filename):
    """Metodo per aggiornare il path"""
    user_id = instance.utente.id if instance.utente else 'default'
    folder_path = os.path.join(MEDIA_ROOT, 'path_prestazione_files', str(user_id))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    full_path = os.path.join(folder_path, filename)
    return full_path


class Prestazione(models.Model):
    """Modello Prestazione"""
    file = models.FileField('Referto', upload_to=upload_to_prestazione, null=True, blank=True)
    note = models.TextField('Note', max_length=100, null=True, blank=True)
    utente = models.ForeignKey(User, verbose_name='paziente', related_name='prestazioni_ricevute',
                               on_delete=models.SET_NULL, null=True, blank=False)
    operatore = models.ForeignKey(User, verbose_name='operatore', related_name='prestazioni_fornite',
                                  on_delete=models.SET_NULL, null=True, blank=False)

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
            new_file_path = upload_to_prestazione(self, os.path.basename(self.file.name))
            existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'path_prestazione_files', str(paziente_id)))

            if os.path.basename(new_file_path) in existing_files:
                raise ValidationError({'file': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})

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
