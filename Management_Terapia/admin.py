from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import Terapia


class TerapiaAdmin(admin.ModelAdmin):
    list_display = ['id', 'note', 'visualizza_file', ]
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

admin.site.register(Terapia, TerapiaAdmin)
