from Healthcare.settings import MEDIA_ROOT
from Management_Terapia.models import get_upload_path
from Management_User.models import HealthCareUser as User
from django.db import models
import os


def upload_to_prestazione(instance, filename):
    user_id = instance.utente.id if instance.utente else 'default'
    folder_path = os.path.join(MEDIA_ROOT, 'path_prestazione_files', str(user_id))

    # Assicurati che la cartella esista
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    full_path = os.path.join(folder_path, filename)
    return full_path


class Prestazione(models.Model):
    file = models.FileField('Referto', upload_to=upload_to_prestazione, null=True, blank=True)
    note = models.TextField('Note', max_length=100, null=True, blank=True)
    utente = models.ForeignKey(User, verbose_name='paziente', related_name='prestazioni_ricevute', on_delete=models.SET_NULL, null=True, blank=True)
    operatore = models.ForeignKey(User, verbose_name='operatore', related_name='prestazioni_fornite', on_delete=models.SET_NULL, null=True, blank=True)

    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        return ''

    # Metodo per stampare a schermo le istanze create
    def __str__(self):
        return f"{self.id}, {self.filename()}, {self.utente}"

# overwrite del metodo save per gestire i file
    def save(self, request=None, *args, **kwargs):

        if self.pk:
            try:
                old_instance = Prestazione.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    # Elimina il file precedente se è stato modificato
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except Prestazione.DoesNotExist:
                pass

            if old_instance.utente != self.utente:
                if old_instance.file:
                    old_file_path = old_instance.file.path
                    if os.path.exists(old_file_path):
                        # Genero il nuovo percorso del file
                        new_path = upload_to_prestazione(self, os.path.basename(self.file.name))
                        # Sposto fisicamente il file nel nuovo percorso
                        os.rename(old_file_path, new_path)
                        # Aggiorno il campo del modello con il nuovo percorso
                        self.file.name = os.path.relpath(new_path, MEDIA_ROOT)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'
