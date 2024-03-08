from django.db import models
import os

def upload_to_prestazione(instance, filename):
    return os.path.join('path_prestazione_files', filename)

class Prestazione(models.Model):
    file = models.FileField('Referto', upload_to=upload_to_prestazione, null=True, blank=True)
    note = models.TextField('Note', max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Prestazione {self.id}: {self.note}"

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
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Prestazione'
        verbose_name_plural = 'Prestazioni'
