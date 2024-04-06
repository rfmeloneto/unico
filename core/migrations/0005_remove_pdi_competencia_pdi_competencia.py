# Generated by Django 5.0 on 2024-04-06 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_formulario_pdi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdi',
            name='competencia',
        ),
        migrations.AddField(
            model_name='pdi',
            name='competencia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pdi_competencias', to='core.competencia'),
        ),
    ]
