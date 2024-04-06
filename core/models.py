import logging
from django.db.transaction import atomic
from core.core_exceptions import EstudanteExceptions
from django.db import models
from django.contrib.auth.models import User
from core.choices import (
    DEFICIENCIA_CHOICES,
    ETAPA_ENSINO_CHOICES,
    SERIE_CHOICES,
    PERFIL_CHOICES,
    LOCALIZACAO_CHOICES,
    DEP_ADM_CHOICES,
    COMPETENCIA_CHOICES,
)

log = logging.getLogger(__name__)
from django.contrib.auth import get_user_model


class Habilidade(models.Model):
    habilidade = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"{self.habilidade}"


class Competencia(models.Model):
    competencia = models.IntegerField(
        choices=COMPETENCIA_CHOICES, blank=False, null=False
    )

    def __str__(self):
        return f"{self.get_competencia_display()}"


class Arquivo(models.Model):
    titulo = models.CharField(max_length=300, blank=False, null=False)
    file = models.FileField(
        blank=True, null=True, upload_to="files/", verbose_name="Arquivo"
    )

    def __str__(self):
        return f"{self.titulo}"


class Perfil(models.Model):
    tipo = models.IntegerField(choices=PERFIL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()}"


class Deficiencia(models.Model):
    deficiencia = models.IntegerField(
        choices=DEFICIENCIA_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.get_deficiencia_display()}"


class Etapa(models.Model):
    etapa = models.IntegerField(choices=ETAPA_ENSINO_CHOICES, blank=True, null=True)
    serie = models.IntegerField(choices=SERIE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.get_etapa_display()} - {self.get_serie_display()}"


class Escola(models.Model):
    nome = models.CharField(
        max_length=300, blank=False, null=False, verbose_name="Escola"
    )
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    localizacao = models.IntegerField(
        choices=LOCALIZACAO_CHOICES, blank=False, null=False
    )
    dep_adm = models.IntegerField(choices=DEP_ADM_CHOICES, blank=False, null=False)
    codigo_inep = models.CharField(max_length=300, blank=False, null=False)
    etapa = models.ManyToManyField(
        Etapa, related_name="escola_etapas", null=True, blank=True
    )

    def __str__(self):
        return f"{self.nome} - {self.get_dep_adm_display()} - {self.get_localizacao_display()}"


class Estudante(models.Model):
    nome = models.CharField(max_length=300, blank=False, null=False)
    escola = models.ForeignKey(
        Escola, on_delete=models.DO_NOTHING, related_name="estudante_escola"
    )
    integrante = models.ManyToManyField(
        "Integrante", related_name="estudante_integrantes", null=True, blank=True
    )
    dificiencia = models.ManyToManyField(
        Deficiencia, related_name="estudante_deficiencias", null=True, blank=True
    )
    pdi = models.ManyToManyField(
        "Pdi", related_name="estudante_pdis", null=True, blank=True
    )
    etapa = models.ForeignKey(
        Etapa,
        on_delete=models.DO_NOTHING,
        related_name="estudante_etapa",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.nome} - {self.escola.nome} - {self.etapa.serie}"


class Integrante(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="integrante_user"
    )
    escola = models.ManyToManyField(Escola, related_name="integrante_escolas")
    perfil = models.ForeignKey(
        Perfil,
        related_name="integrante_perfil",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.first_name} - {[escola for escola in self.escola.all()]} - {self.perfil.get_tipo_display()}"


class Pdi(models.Model):
    titulo = models.CharField(max_length=300, null=False, blank=False)
    data_inicial = models.DateField()
    data_final = models.DateField()
    descricao = models.TextField(null=False, blank=False)
    competencia = models.ForeignKey(
        Competencia,
        related_name="pdi_competencias",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
    )

    estudante = models.ForeignKey(
        Estudante, on_delete=models.CASCADE, related_name="pdi_estudante"
    )
    integrante = models.ManyToManyField("Integrante")
    ativo = models.BooleanField(default=True)
    concluido = models.BooleanField(default=False)
    arquivo = models.ForeignKey(
        Arquivo,
        related_name="pdi_arquivo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.titulo}"

    def save(self, *args, **kwargs):
        if self.data_final < self.data_inicial:
            print("A data final não pode ser maior que a incial")
            return "A data final não pode ser maior que a incial"
        else:
            super().save(*args, **kwargs)


class Comunicacao(models.Model):
    autor = models.ForeignKey("Integrante", on_delete=models.CASCADE)
    menssagem = models.TextField(blank=False, null=False)
    pdi = models.ForeignKey(
        "Pdi", related_name="comunicacao_pdi", on_delete=models.CASCADE
    )
    arquivo = models.ForeignKey(
        Arquivo,
        related_name="comunicacao_arquivo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.autor} {self.menssagem[:20]}"


class Avaliacao(models.Model):
    pdi = models.ForeignKey(
        "Pdi", related_name="avaliacao_pdi", on_delete=models.CASCADE
    )
    formulario = models.ManyToManyField(
        "Formulario", related_name="avaliacao_formularios"
    )
    arquivo = models.ForeignKey(
        Arquivo,
        related_name="avaliacao_arquivo",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.pdi} {self.arquivo}"


class Formulario(models.Model):
    pdi = models.ForeignKey(
        "Pdi",
        related_name="formulario_pdi",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    habilidade = models.ForeignKey(
        "Habilidade", related_name="formulario_habilidade", on_delete=models.CASCADE
    )
    competencia = models.ForeignKey(
        "Competencia", related_name="formulario_competencia", on_delete=models.CASCADE
    )
    nota = models.IntegerField(default=0)
    estrategia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pdi}"
