from django import forms
from .models import Pdi, Formulario
from django.forms import inlineformset_factory


class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ["habilidade", "competencia", "estrategia", "nota"]


class PdiForm(forms.ModelForm):
    class Meta:
        model = Pdi
        fields = [
            "titulo",
            "data_inicial",
            "data_final",
            "descricao",
            "competencia",
            "habilidade",
            "arquivo",
            "ativo",
            "concluido",
        ]


FormularioFormSet = inlineformset_factory(Pdi, Formulario, form=FormularioForm, extra=1)
