# Generated by Django 5.0 on 2024-04-17 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_avaliacao_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='nota',
            field=models.IntegerField(choices=[(1, 'Muito Satisfatório'), (2, 'Satisfatorio'), (3, 'Indiferente'), (4, 'Insatisfatorio'), (5, 'Muito Insatisfatorio')], default=5),
            preserve_default=False,
        ),
    ]
