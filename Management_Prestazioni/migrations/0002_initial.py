# Generated by Django 5.0.3 on 2024-03-19 15:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Management_Prestazioni', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='prestazione',
            name='operatore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestazioni_fornite', to=settings.AUTH_USER_MODEL, verbose_name='operatore'),
        ),
        migrations.AddField(
            model_name='prestazione',
            name='utente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestazioni_ricevute', to=settings.AUTH_USER_MODEL, verbose_name='paziente'),
        ),
    ]