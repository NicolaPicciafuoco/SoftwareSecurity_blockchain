from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import Terapia
from Management_User.models import HealthCareUser as User

class TerapiaAdmin(admin.ModelAdmin):
    list_display = ['note', 'visualizza_file', ]
    actions = ['clear_selected_files']

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
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Disabilita la possibilità di scegliere il prescrittore nella form
        form.base_fields['prescrittore'].widget.attrs['disabled'] = True
        form.base_fields['prescrittore'].widget.attrs['display'] = False
        return form


admin.site.register(Terapia, TerapiaAdmin)
