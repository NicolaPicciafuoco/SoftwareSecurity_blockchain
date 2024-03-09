from django.db import models
import os
from django.contrib.auth.models import User

from Healthcare.settings import MEDIA_ROOT
def get_upload_path(instance, filename):
    user_id = instance.utente.id if instance.utente else 'default'
    print(f"ID dell'istanza: {user_id}")
    folder_path = os.path.join(MEDIA_ROOT, 'file_terapia', str(user_id))

    # Controlla se la cartella esiste
    if not os.path.exists(folder_path):
        # Crea la cartella se non esiste
        os.makedirs(folder_path, exist_ok=True)

    full_path = os.path.join(folder_path, filename)
    print(f"Percorso completo del file: {full_path}")

    return full_path


class Terapia(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    file = models.FileField('Terapia', upload_to=get_upload_path, null=True, blank=True)
    note = models.CharField('note', max_length=100, null=True, blank=True)

    def delete_file(self):
        # Verifica se il file esiste e lo elimina
        if self.file:
            path = self.file.path
            if os.path.exists(path):
                os.remove(path)
            self.file.delete()

    def save(self, *args, **kwargs):
        # Se è un'istanza esistente e il file è stato cambiato, elimina il vecchio file
        if self.pk:
            try:
                old_instance = Terapia.objects.get(pk=self.pk)
                if old_instance.file and self.file != old_instance.file:
                    # Elimina il file precedente se è stato modificato
                    if os.path.isfile(old_instance.file.path):
                        os.remove(old_instance.file.path)
            except Terapia.DoesNotExist:
                pass
        super().save(*args, **kwargs)




    def __str__(self):
        return f"Terapia {self.id}: {self.note}"

    class Meta:
        verbose_name_plural = "Terapie"
