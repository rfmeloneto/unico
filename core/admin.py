from django.contrib import admin

from .models import Escola, Perfil, Estudante, Integrante, Pdi, Comunicacao, Arquivo

admin.site.register(Escola)
admin.site.register(Perfil)
admin.site.register(Estudante)
admin.site.register(Integrante)
admin.site.register(Pdi)
admin.site.register(Comunicacao)
admin.site.register(Arquivo)

admin.site.site_header = 'Sistema de Gerenciamento Único'

