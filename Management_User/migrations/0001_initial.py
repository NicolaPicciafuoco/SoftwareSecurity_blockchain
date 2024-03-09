# Generated by Django 5.0.2 on 2024-03-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthCareUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'Questa e-mail è già in uso'}, max_length=254, unique=True, verbose_name='indirizzo e-mail')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome')),
                ('cognome', models.CharField(blank=True, max_length=150, null=True, verbose_name='Cognome')),
                ('sesso', models.SmallIntegerField(choices=[(1, 'Maschio'), (2, 'Femmina')], default=1)),
                ('data_nascita', models.DateField(verbose_name='Data di nascita')),
                ('luogo_nascita', models.CharField(blank=True, max_length=200, null=True, verbose_name='Luogo nascita')),
                ('telefono', models.CharField(blank=True, max_length=14, null=True, verbose_name='Numero di telefono')),
                ('codice_fiscale', models.CharField(blank=True, max_length=16, null=True, verbose_name='Codice fiscale')),
                ('indirizzo_residenza', models.CharField(blank=True, max_length=255, null=True, verbose_name='Indirizzo  di residenza')),
                ('indirizzo_domicilio', models.CharField(blank=True, max_length=255, null=True, verbose_name='Indirizzo di domicilio')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='attivo')),
                ('data_creazione', models.DateTimeField(auto_now_add=True, verbose_name='Data di creazione')),
                ('data_modifica', models.DateTimeField(auto_now=True, verbose_name='Data di aggiornamento')),
                ('groups', models.ManyToManyField(blank=True, related_name='telmed_user_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='telmed_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Utente',
                'verbose_name_plural': 'Utenti',
            },
        ),
    ]
