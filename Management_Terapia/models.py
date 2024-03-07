from django.db import models
from datetime import datetime
# Create your models here.

class Terapia(models.Model):
    file = models.FileField('Terapia',upload_to='path_terapie_files/', null=True, blank=True)
    note = models.CharField('note', max_length=100, null=True, blank=True)
    # paziente = models.ForeignKey(Paziente, on_delete=models.CASCADE)
    # medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Terapia {self.id}: {self.note}"

    class Meta:
        verbose_name_plural = "Terapie"
