# Generated by Django 5.0 on 2024-04-06 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_pdi_competencia_pdi_competencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdi',
            name='habilidade',
        ),
    ]
