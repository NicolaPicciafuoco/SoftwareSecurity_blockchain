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
    actions = ['custom_delete_selected']

    def delete(self, *args, **kwargs):
        print("delete1")
        # Esegui operazioni personalizzate prima dell'eliminazione
        self.delete_file()  # Chiamata a una funzione personalizzata per eliminare il file associato

        # Chiamata al metodo delete della classe padre per eseguire l'eliminazione effettiva dal database
        super().delete(*args, **kwargs)

    def delete_file(self):
        print("delete2")
        # Funzione personalizzata per eliminare il file associato, ad esempio:
        if self.file:
            print("delete3")
            file_path = os.path.join(settings.MEDIA_ROOT, str(self.file))
            if os.path.exists(file_path):
                print("delete4")
                os.remove(file_path)



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



    def save_model(self, request, obj, form, change):
        'funzione per il salvataggio del modello'
        obj.prescrittore = request.user
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

    def custom_delete_selected(self, request, queryset):
        for terapia in queryset:
            # Chiamare il tuo metodo delete_file personalizzato per ogni terapia
            terapia.delete_file()
            # Eliminare la terapia
            terapia.delete()

    custom_delete_selected.short_description = "Elimina terapie"

    # sovrascrittura per  il metodo get_actions per rimuovere l'azione di eliminazione predefinita
    def get_actions(self, request):
        actions = super().get_actions(request)
        # Rimuovi l'azione di eliminazione predefinita
        del actions['delete_selected']
        return actions

admin.site.register(Terapia, TerapiaAdmin)
