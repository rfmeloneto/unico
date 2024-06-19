from django import forms

from core.choices import AVALIAR_PDI_CHOICES
from .models import Pdi, Formulario, Comunicacao, Avaliacao

NOTA_CHOICES = [(i, str(i)) for i in range(11)]


class FormularioForm(forms.ModelForm):
    nota = forms.TypedChoiceField(
        choices=NOTA_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Formulario
        fields = ["habilidade", "competencia", "estrategia", "nota"]
        widgets = {
            "habilidade": forms.Select(attrs={"class": "form-control"}),
            "competencia": forms.Select(attrs={"class": "form-control"}),
            "estrategia": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 100}
            ),
            # "nota": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "habilidade": "Habilidade",
            "competencia": "Competência",
            "estrategia": "Estratégia",
            "nota": "Nota",
        }


class PdiForm(forms.ModelForm):
    data_inicial = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={
                "class": "form-control",
                "type": "text",  # Usar "text" para permitir customização do formato de exibição
                "placeholder": "dd/mm/yyyy",
            },
        ),
    )
    data_final = forms.DateField(
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={
                "class": "form-control",
                "type": "text",  # Usar "text" para permitir customização do formato de exibição
                "placeholder": "dd/mm/yyyy",
            },
        ),
    )

    class Meta:
        model = Pdi
        fields = [
            "titulo",
            "data_inicial",
            "data_final",
            "descricao",
            "competencia",
            "arquivo",
            "ativo",
            "concluido",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 100},
            ),
            "competencia": forms.Select(attrs={"class": "form-control"}),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(),
            "concluido": forms.CheckboxInput(),
        }
        labels = {
            "titulo": "Título",
            "data_inicial": "Data Inicial",
            "data_final": "Data Final",
            "descricao": "Descrição",
            "arquivo": "Arquivo",
            "ativo": "Ativo",
            "concluido": "Concluído",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Formatando as datas iniciais para a exibição no formulário
            self.fields["data_inicial"].initial = self.instance.data_inicial.strftime(
                "%d/%m/%Y"
            )
            self.fields["data_final"].initial = self.instance.data_final.strftime(
                "%d/%m/%Y"
            )


class PdiEditForm(forms.ModelForm):
    class Meta:
        model = Pdi
        fields = [
            "titulo",
            "descricao",
            "competencia",
            "arquivo",
            "ativo",
            "concluido",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 100},
            ),
            "competencia": forms.Select(attrs={"class": "form-control"}),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(),
            "concluido": forms.CheckboxInput(),
        }
        labels = {
            "titulo": "Título",
            "descricao": "Descrição",
            "arquivo": "Arquivo",
            "ativo": "Ativo",
            "concluido": "Concluído",
        }


class ComunicacaoForm(forms.ModelForm):
    class Meta:
        model = Comunicacao
        fields = ["menssagem", "arquivo"]
        widgets = {
            "menssagem": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 100}
            ),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "menssagem": "Menssagem",
            "arquivo": "Arquivo",
        }


class AvaliacaoForm(forms.ModelForm):
    nota = forms.ChoiceField(
        choices=AVALIAR_PDI_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Avaliacao
        fields = ["comentario", "arquivo"]
        widgets = {
            "comentario": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 100}
            ),
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "comentario": "comentario",
            "arquivo": "Arquivo",
        }
