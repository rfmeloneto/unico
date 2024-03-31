# Generated by Django 5.0 on 2024-03-29 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competencia',
            name='competencia',
            field=models.IntegerField(choices=[(1, 'Conhecimento'), (2, 'Pensamento científico, crítico e criativo'), (3, 'Senso estético e repertório cultural'), (4, 'Comunicação'), (5, 'Cultura digital'), (6, 'Reconhecimento'), (7, 'Autogestão'), (8, 'Autonomia'), (9, 'Autoconhecimento e autocuidado'), (10, 'Empatia e cooperação')]),
        ),
        migrations.AlterField(
            model_name='deficiencia',
            name='deficiencia',
            field=models.IntegerField(blank=True, choices=[(1, 'Baixa Visão'), (2, 'Cegueira'), (3, 'Visão Monocular'), (4, 'Deficiência Auditiva'), (5, 'Deficiência Física'), (6, 'deficiência intelectual'), (7, 'Surdez'), (8, 'Surdocegueira'), (9, 'Transtorno do Espectro Autista (TEA)'), (10, 'Altas Habilidades ou Superdotação')], null=True),
        ),
        migrations.AlterField(
            model_name='escola',
            name='dep_adm',
            field=models.IntegerField(choices=[(1, 'Municiapal'), (2, 'Estadual')]),
        ),
        migrations.AlterField(
            model_name='escola',
            name='localizacao',
            field=models.IntegerField(choices=[(1, 'Rural'), (2, 'Urbana')]),
        ),
        migrations.AlterField(
            model_name='etapa',
            name='etapa',
            field=models.IntegerField(blank=True, choices=[(1, 'Ensino Fundamental Anos Iniciais'), (2, 'Ensino Fundamental Anos Finais'), (3, 'Ensino Medio')], null=True),
        ),
        migrations.AlterField(
            model_name='etapa',
            name='serie',
            field=models.IntegerField(blank=True, choices=[(1, '1 Ano'), (2, '2 Ano'), (3, '3 Ano'), (4, '4 Ano'), (5, '5 Ano'), (6, '6 Ano'), (7, '7 Ano'), (8, '8 Ano'), (9, '9 Ano'), (10, '1 Série'), (11, '2 Série'), (12, '3 Série')], null=True),
        ),
    ]