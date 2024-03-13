# Generated by Django 5.0.2 on 2024-03-13 11:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management_User', '0005_remove_healthcareuser_caregiver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthcareuser',
            name='in_cura_da',
            field=models.ManyToManyField(blank=True, related_name='pazienti_assegnati', to=settings.AUTH_USER_MODEL, verbose_name='In cura da'),
        ),
    ]
