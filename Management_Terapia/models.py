from django.core.exceptions import ValidationError
from Management_User.models import HealthCareUser as User
from Healthcare.settings import MEDIA_ROOT
from django.db import models
import os


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
        if self.pk:
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
        super().save(*args, **kwargs)

    def __str__(self):
        ''' il ritorno della stringa'''
        return f"Terapia {self.pk}: {self.note}"

    class Meta:
        ''' per il nome plurale'''
        verbose_name_plural = "Terapie"
