from django.db import models

class Prestazione(models.Model):

    file = models.FileField('Referto', null=True, blank=True)

    note = models.TextField('Note', null=True, blank=True)

    def __str__(self):
        return f"Prestazione {self.id}: {self.note}"
    class Meta:
        verbose_name='Prestazione'
        verbose_name_plural='Prestazioni'



