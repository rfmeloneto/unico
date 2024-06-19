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


class EscolaAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Escola"


class PerfilAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Perfil"


class EstudanteAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Estudante"


class IntegranteAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Integrantes da Equipe"


class PdiAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Pdis"


class ComunicacaoAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Comunicação"


class ArquivoAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Arquivos"


class CompetenciaAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Competência"


class HabilidadeAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Habilidades"


class DeficienciaAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Deficiência"


class FormularioAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Formulário de Atividade"


class AvaliacaoAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Avaliação do PDI"


class EtapaAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Cadastro de Etapa de Ensino"


admin.site.register(Escola, EscolaAdmin)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Estudante, EstudanteAdmin)
admin.site.register(Integrante, IntegranteAdmin)
admin.site.register(Pdi, PdiAdmin)
admin.site.register(Comunicacao, ComunicacaoAdmin)
admin.site.register(Arquivo, ArquivoAdmin)
admin.site.register(Competencia, CompetenciaAdmin)
admin.site.register(Habilidade, HabilidadeAdmin)
admin.site.register(Deficiencia, DeficienciaAdmin)
admin.site.register(Formulario, FormularioAdmin)
admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Etapa, EtapaAdmin)


admin.site.site_header = "Sistema de Gerenciamento Único"
