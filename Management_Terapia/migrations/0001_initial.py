# Generated by Django 5.0.2 on 2024-03-07 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Terapia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='file/', verbose_name='Terapia')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='note')),
            ],
            options={
                'verbose_name_plural': 'Terapie',
            },
        ),
    ]
