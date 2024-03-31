from django import forms
from .models import Pdi, Formulario, Competencia, Habilidade
from django.forms import inlineformset_factory


# class FormularioForm(forms.ModelForm):
#     class Meta:
#         model = Formulario
#         fields = ["habilidade", "competencia", "estrategia", "nota"]
#         widgets = {
#             "habilidade": forms.Select(attrs={"class": "form-control"}),
#             "competencia": forms.Select(attrs={"class": "form-control"}),
#             "estrategia": forms.Textarea(
#                 attrs={"class": "form-control custom-textarea", "rows": 10}
#             ),
#             "nota": forms.NumberInput(attrs={"class": "form-control"}),
#         }
#         labels = {
#             "habilidade": "Habilidade",
#             "competencia": "Competência",
#             "estrategia": "Estratégia",
#             "nota": "Nota",
#         }


# class PdiForm(forms.ModelForm):
#     class Meta:
#         model = Pdi
#         fields = [
#             "titulo",
#             "data_inicial",
#             "data_final",
#             "descricao",
#             "competencia",
#             "habilidade",
#             "arquivo",
#             "ativo",
#             "concluido",
#         ]
#         widgets = {
#             "titulo": forms.TextInput(attrs={"class": "form-control"}),
#             "data_inicial": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#             "data_final": forms.DateInput(
#                 attrs={"class": "form-control", "type": "date"}
#             ),
#             "descricao": forms.Textarea(
#                 attrs={"class": "form-control custom-textarea", "rows": 10}
#             ),
#             "competencia": forms.SelectMultiple(attrs={"class": "form-control"}),
#             "habilidade": forms.SelectMultiple(attrs={"class": "form-control"}),
#             "arquivo": forms.FileInput(attrs={"class": "form-control"}),
#             "ativo": forms.CheckboxInput(),
#             "concluido": forms.CheckboxInput(),
#         }
#         labels = {
#             "titulo": "Título",
#             "data_inicial": "Data Inicial",
#             "data_final": "Data Final",
#             "descricao": "Descrição",
#             "competencia": "Competência",
#             "habilidade": "Habilidade",
#             "arquivo": "Arquivo",
#             "ativo": "Ativo",
#             "concluido": "Concluído",
#         }


class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ["habilidade", "competencia", "estrategia", "nota"]
        widgets = {
            "habilidade": forms.Select(attrs={"class": "form-control"}),
            "competencia": forms.Select(attrs={"class": "form-control"}),
            "estrategia": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 10}
            ),
            "nota": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "habilidade": "Habilidade",
            "competencia": "Competência",
            "estrategia": "Estratégia",
            "nota": "Nota",
        }


class PdiForm(forms.ModelForm):
    competencia = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False,
    )
    habilidade = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Pdi
        fields = [
            "titulo",
            "data_inicial",
            "data_final",
            "descricao",
            "arquivo",
            "ativo",
            "concluido",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "data_inicial": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_final": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "descricao": forms.Textarea(
                attrs={"class": "form-control custom-textarea", "rows": 10}
            ),
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
        self.fields["competencia"].queryset = Competencia.objects.all()
        self.fields["habilidade"].queryset = Habilidade.objects.all()


FormularioFormSet = inlineformset_factory(Pdi, Formulario, form=FormularioForm, extra=1)
