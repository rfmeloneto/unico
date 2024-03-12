# Generated by Django 5.0 on 2023-12-09 19:01

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
            name='Arquivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('file', models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Arquivo')),
            ],
        ),
        migrations.CreateModel(
            name='Escola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300, verbose_name='Escola')),
            ],
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(1, 'Administrador Master'), (2, 'Administrador'), (3, 'Professor'), (4, 'Estudante'), (5, 'Saúde')])),
            ],
        ),
        migrations.CreateModel(
            name='Estudante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.escola')),
            ],
        ),
        migrations.CreateModel(
            name='Integrante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=300)),
                ('escola', models.ManyToManyField(blank=True, null=True, related_name='integrante_escolar', to='core.escola')),
                ('estudante', models.ManyToManyField(blank=True, null=True, related_name='integrante_estudante', to='core.estudante')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_integrante', to='core.perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Pdi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('data_inicial', models.DateField()),
                ('data_final', models.DateField()),
                ('descricao', models.TextField()),
                ('ativo', models.BooleanField(default=True)),
                ('concluido', models.BooleanField(default=False)),
                ('arquivo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.arquivo')),
                ('estudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estudante_pdi', to='core.estudante')),
                ('integrante', models.ManyToManyField(to='core.integrante')),
            ],
        ),
    ]
