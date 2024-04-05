from django.contrib import messages


# def assegna_permessi(self, request, queryset):
#     print("assegna_permessi called")  # Debugging
#     selected_count = queryset.count()
#     print(f"Number of selected items: {selected_count}")  # Debugging
#     self.message_user(
#         request,
#         f"{selected_count} selezione",
#         messages.SUCCESS,
#     )


assegna_permessi.short_description = "assegna permessi"
# print("\n\n\n\n")
# content_type_user = apps.get_model(HealthCareUser, require_ready=True)
# all_permissions_user = Permission.objects.filter(content_type=content_type_user)
# print(f"user permission: {all_permissions_user}")
# print("\n\n\n\n")
# print("\n\n\n\n")
# content_type_terapia = ContentType.objects.get_for_model(Terapia)
# all_permissions_terapia = Permission.objects.filter(content_type=content_type_terapia)
# print(f"terapia permission: {all_permissions_terapia}")
# print("\n\n\n\n")
#
# print("\n\n\n\n")
# content_type_prestazione = ContentType.objects.get_for_model(Prestazione)
# all_permissions_prestazione = Permission.objects.filter(content_type=content_type_prestazione)
# print(f"prestazione permission: {all_permissions_prestazione}")
# print("\n\n\n\n")
