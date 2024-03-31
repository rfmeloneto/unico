# Generated by Django 5.0 on 2024-03-31 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_integrante_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='pdi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formulario_pdi', to='core.pdi'),
        ),
    ]