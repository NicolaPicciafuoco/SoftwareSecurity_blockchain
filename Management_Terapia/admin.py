from django.contrib import admin
from django.forms import ModelForm, forms
from django.utils.html import format_html
from django.conf import settings
from django.core.exceptions import ValidationError
from Healthcare.settings import MEDIA_ROOT
from .models import Terapia, get_upload_path
import os


class TerapiaAdminForm(ModelForm):
    class Meta:
        model = Terapia
        fields = '__all__'


class TerapiaAdmin(admin.ModelAdmin):
    form = TerapiaAdminForm
    list_display = ['note', 'visualizza_file', ]
    actions = ['clear_selected_files']

    def delete_model(self, request, obj):
        # Chiamare il metodo delete_file per eliminare il file associato
        obj.delete_file()
        # Eliminare l'istanza di Terapia
        obj.delete()

    def visualizza_file(self, obj):
        if obj.file:
            file_url = obj.file.url
            return format_html('<a href="{}" target="_blank">Visualizza</a>', file_url)
        else:
            return "Nessun file"

    visualizza_file.short_description = "File"

    @admin.action(description='Elimina il file')
    def clear_selected_files(modeladmin, request, queryset):
        # Verifica se DEBUG è True prima di procedere
        # Verifica se il degab è uguale a true, verificare se funziona quando viene dockerizzato.
        if settings.DEBUG:
            for terapia in queryset:
                terapia.delete_file()

    clear_selected_files.short_description = "Elimina il file"

    def save_model(self, request, obj, form, change):
        # Imposta l'utente corrente come prescrittore
        obj.prescrittore = request.user
        # Controlla il conflitto del nome del file
        if obj.file:
            paziente_id = getattr(obj.utente, 'id', None)
            new_file_path = get_upload_path(obj, os.path.basename(obj.file.name))
            existing_files = os.listdir(os.path.join(MEDIA_ROOT, 'file_terapia', str(paziente_id)))
            if os.path.basename(new_file_path) in existing_files:
                raise ValidationError({'file_id': ['Il file con lo stesso nome esiste già. Scegli un nome diverso.']})

        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Disabilita la possibilità di scegliere il prescrittore nella form
        form.base_fields['prescrittore'].widget.attrs['disabled'] = True
        form.base_fields['prescrittore'].widget.attrs['style'] = 'display: none;'
        return form


admin.site.register(Terapia, TerapiaAdmin)
