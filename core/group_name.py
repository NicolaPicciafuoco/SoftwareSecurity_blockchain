"""
GROUP_PAZIENTE
    è un utente che riceve le terapie e le prestazioni non che gli viene assegnato il caregiver
    CRUD
    _X__ terapie
    __X_ le info del utente
    XXXX prestazioni [solo per quelle create da lui le altre le può solo leggere]

GROUP_CAREGIVER
    è un utente svolge le prestazioni solo per un paziente che gli viene assegnato
            e si chiamerà assistito (il paziente)
    CRUD
    _X__ terapie
    _X__ le info del paziente
    XXXX prestazioni [solo per quelle create da lui le altre le può solo leggere]

GROUP_DOTTORE
    è un utente prescrive una terapia per tutti i pazienti
    CRUD
    XXXX terapie [solo per quelle create da lui le altre le può solo leggere]
    _X__ le info del paziente
    XXXX prestazioni [solo per quelle create da lui le altre le può solo leggere]

GROUP_DOTTORE_SPECIALISTA
    è un utente prescrive una terapia per tutti i pazienti
    CRUD
    XXXX terapie [solo per quelle create da lui le altre le può solo leggere]
    _X__ le info del paziente
    XXXX prestazioni [solo per quelle create da lui le altre le può solo leggere]

GROUP_AMMINISTRATORE
    è un utente che gestisce la piattaforma ed eventuali problemi
    CRUD
    XXXX terapie [solo superuser]
    XXXX le info del utente
    XXXX prestazioni [solo superuser]
    XXXX gruppi [solo superuser]

"""
GROUP_PAZIENTE: str = 'Paziente'
GROUP_CAREGIVER: str = 'Caregiver'
GROUP_DOTTORE: str = 'Dottore'
GROUP_DOTTORE_SPECIALISTA: str = 'Dottore Specialista'
GROUP_AMMINISTRATORE: str = 'Amministratore'
