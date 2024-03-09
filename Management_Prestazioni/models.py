from Healthcare.settings import MEDIA_ROOT
from django.contrib.auth.models import User
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
    def save(self, *args, **kwargs):
        # Controlla se il campo FileField è stato pulito e il file associato esiste
        if self.pk:
            try:
                old_instance = Prestazione.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    # Elimina il file precedente se è stato modificato
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except Prestazione.DoesNotExist:
                pass
        # Richiamo il metodo save della classe base per salvare la modifica
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'
