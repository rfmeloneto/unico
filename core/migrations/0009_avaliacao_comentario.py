# Generated by Django 5.0 on 2024-04-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_comunicacao_menssagem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='comentario',
            field=models.TextField(blank=True, null=True),
        ),
    ]
