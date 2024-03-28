from django.db import models
from django.contrib.auth.models import User
from core.choices import (
    DEFICIENCIA_CHOICES,
    ETAPA_ENSINO_CHOICES,
    SERIE_CHOICES,
    PERFIL_CHOICES,
    LOCALIZACAO_CHOICES,
    DEP_ADM_CHOICES,
)


class Habilidade(models.Model):
    habilidade = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"{self.habilidade}"


class Competencia(models.Model):
    competencia = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"{self.competencia}"


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
    deficiencia = models.CharField(
        max_length=300, choices=DEFICIENCIA_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.get_deficiencia_display()}"


class Etapa(models.Model):
    etapa = models.CharField(
        max_length=300, choices=ETAPA_ENSINO_CHOICES, blank=True, null=True
    )
    serie = models.CharField(
        max_length=300, choices=SERIE_CHOICES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.get_etapa_display() - self.get_serie_display()}"


class Escola(models.Model):
    nome = models.CharField(
        max_length=300, blank=False, null=False, verbose_name="Escola"
    )
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    localizacao = models.CharField(
        choices=LOCALIZACAO_CHOICES, max_length=300, blank=False, null=False
    )
    dep_adm = models.CharField(
        choices=DEP_ADM_CHOICES, max_length=300, blank=False, null=False
    )
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
        return f"{self.nome} - {self.escola.nome} - {self.get_etapa.serie_display()}"


class Integrante(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="integrante_user"
    )
    escola = models.ManyToManyField(Escola, related_name="integrante_escolas")
    nome = models.CharField(max_length=300, blank=False, null=False)
    perfil = models.ForeignKey(
        Perfil,
        related_name="integrante_perfil",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.nome} - {self.escola.nome} - {self.get_perfil_display()}"


class Pdi(models.Model):
    titulo = models.CharField(max_length=300, null=False, blank=False)
    data_inicial = models.DateField()
    data_final = models.DateField()
    descricao = models.TextField(null=False, blank=False)
    habilidade = models.ManyToManyField(
        Habilidade, related_name="pdi_habilidades", blank=True, null=True
    )
    competencia = models.ManyToManyField(
        Competencia, related_name="pdi_competencias", blank=True, null=True
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
    habilidade = models.ForeignKey(
        "Habilidade", related_name="formulario_habilidade", on_delete=models.CASCADE
    )
    competencia = models.ForeignKey(
        "Competencia", related_name="formulario_competencia", on_delete=models.CASCADE
    )
    nota = models.IntegerField(default=0)
    estrategia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.pdi} {self.arquivo}"
