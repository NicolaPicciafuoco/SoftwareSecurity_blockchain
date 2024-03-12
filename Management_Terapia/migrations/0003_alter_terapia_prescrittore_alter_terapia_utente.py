# Generated by Django 5.0.2 on 2024-03-09 17:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_Terapia', '0002_terapia_prescrittore_alter_terapia_utente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='terapia',
            name='prescrittore',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='terapie_prescritte', to=settings.AUTH_USER_MODEL, verbose_name='prescrittore'),
        ),
        migrations.AlterField(
            model_name='terapia',
            name='utente',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='terapie', to=settings.AUTH_USER_MODEL, verbose_name='paziente'),
        ),
    ]