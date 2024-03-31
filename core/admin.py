from django.contrib import admin

from .models import (
    Escola,
    Perfil,
    Estudante,
    Integrante,
    Pdi,
    Comunicacao,
    Arquivo,
    Competencia,
    Habilidade,
    Deficiencia,
    Formulario,
    Avaliacao,
    Etapa,
)

admin.site.register(Escola)
admin.site.register(Perfil)
admin.site.register(Estudante)
admin.site.register(Integrante)
admin.site.register(Pdi)
admin.site.register(Comunicacao)
admin.site.register(Arquivo)
admin.site.register(Competencia)
admin.site.register(Habilidade)
admin.site.register(Deficiencia)
admin.site.register(Formulario)
admin.site.register(Avaliacao)
admin.site.register(Etapa)

admin.site.site_header = "Sistema de Gerenciamento Único"
