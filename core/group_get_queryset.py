"""
In questo file si trovano le funzioni che gestiscono i queryset
che ogni utente può vedere nella propria pagina admin
"""
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from core.group_name import (GROUP_INFERMIERE,
                             GROUP_DOTTORE,
                             GROUP_DOTTORE_SPECIALISTA,
                             GROUP_AMMINISTRATORE,
                             GROUP_CAREGIVER,
                             GROUP_PAZIENTE)


def return_queryset_user(self, request, modello_admin):
    """ Ritorna il queryset corretto per il model admin HealtCareUser"""
    user_group = request.user.groups.all().first()
    all_qs = super(modello_admin, self).get_queryset(request)

    if user_group.name == GROUP_AMMINISTRATORE:
        qs = all_qs

    elif user_group.name == GROUP_PAZIENTE:
        qs = all_qs.filter(id=request.user.id, groups=Group.objects.get(name=GROUP_PAZIENTE).id)

    elif user_group.name == GROUP_CAREGIVER:
        qs = all_qs.filter(
            id__in=[request.user.id, request.user.assistito.id if request.user.assistito else None]
        )

    elif user_group.name == GROUP_INFERMIERE:
        qs = all_qs.filter(
            groups__in=[Group.objects.get(name=GROUP_PAZIENTE).id, ],
        )

    elif user_group.name == GROUP_DOTTORE:
        qs = all_qs.filter(groups__in=[
            Group.objects.get(name=GROUP_PAZIENTE).id,
            Group.objects.get(name=GROUP_INFERMIERE).id,
            Group.objects.get(name=GROUP_CAREGIVER).id
        ])

    elif user_group.name == GROUP_DOTTORE_SPECIALISTA:
        qs = all_qs.filter(groups=Group.objects.get(name=GROUP_PAZIENTE).id)

    else:
        raise PermissionDenied()
    return qs


def return_queryset_terapia(self, request, modello_admin):
    """ Ritorna il queryset corretto per il model admin Terapia"""
    user_group = request.user.groups.all().first()
    all_qs = super(modello_admin, self).get_queryset(request)

    if user_group.name == GROUP_AMMINISTRATORE:
        qs = all_qs

    elif user_group.name == GROUP_PAZIENTE:
        qs = all_qs.filter(utente__id=request.user.id,)

    elif user_group.name == GROUP_CAREGIVER:
        qs = all_qs.filter(
            utente__id__in=[
                request.user.id,
                request.user.assistito.id if request.user.assistito else None
            ],
            utente__groups=Group.objects.get(name=GROUP_PAZIENTE).id
        )

    elif user_group.name == GROUP_INFERMIERE:
        qs = all_qs.filter(utente__groups=Group.objects.get(name=GROUP_PAZIENTE).id)

    elif user_group.name == GROUP_DOTTORE:
        qs = all_qs.filter(utente__groups=Group.objects.get(name=GROUP_PAZIENTE).id)

    elif user_group.name == GROUP_DOTTORE_SPECIALISTA:
        qs = all_qs.filter(utente__groups=Group.objects.get(name=GROUP_PAZIENTE).id,
                           prescrittore__id=request.user.id)

    else:
        raise PermissionDenied()

    return qs