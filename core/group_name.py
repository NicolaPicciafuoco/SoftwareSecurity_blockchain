"""

GROUP_PAZIENTE
    è un utente che riceve le terapie e le prestazioni non che gli viene assegnato il caregiver
    CRUD
    _X__ terapie
    __X_ le info del utente
    _X__ prestazioni che gli sono state fatte todo da aggiungere anche la possibilità di creare una prestazione?

GROUP_CAREGIVER
    è un utente svolge le prestazioni solo per un paziente che gli viene assegnato
            e si chiamerà assistito (il paziente)
    CRUD
    _X__ terapie
    _X__ le info del paziente
    XX__ prestazioni

GROUP_INFERMIERE todo da eliminare?
    è un utente svolge le prestazioni per tutti i pazienti
    CRUD
    _X__ terapie
    _X__ le info del paziente
    XX__ prestazioni

GROUP_DOTTORE
    è un utente prescrive una terapia per tutti i pazienti
    CRUD
    XX__ terapie
    _X__ le info del paziente
    XX__ prestazioni

GROUP_DOTTORE_SPECIALISTA todo da eliminare?
    è un utente prescrive una terapia per tutti i pazienti
    CRUD
    _X__ terapie todo gli interessa crearle o altro?
    _X__ le info del paziente
    XX__ prestazioni

GROUP_AMMINISTRATORE
    è un utente che gestisce la piattaforma ed eventuali problemi
    CRUD
    XXXX terapie
    XXXX le info del utente
    XXXX prestazioni
    XXXX gruppi

"""
GROUP_PAZIENTE: str = 'Paziente'
GROUP_CAREGIVER: str = 'Caregiver'
GROUP_INFERMIERE: str = 'Infermiere'
GROUP_DOTTORE: str = 'Dottore'
GROUP_DOTTORE_SPECIALISTA: str = 'Dottore Specialista'
GROUP_AMMINISTRATORE: str = 'Amministratore'

