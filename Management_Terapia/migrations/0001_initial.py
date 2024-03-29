# Generated by Django 5.0.2 on 2024-03-10 15:09

import Management_Terapia.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Terapia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=Management_Terapia.models.get_upload_path, verbose_name='Terapia')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='note')),
                ('utente', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Terapie',
            },
        ),
    ]
