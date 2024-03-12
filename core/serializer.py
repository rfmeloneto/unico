from rest_framework import serializers
from .models import Arquivo, Escola, Perfil, Estudante, Integrante, Pdi, Comunicacao, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class PdiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdi
        fields = '__all__'

class IntegranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integrante
        fields = ['user', 'nome', 'perfil', 'escola', 'estudante']
        

class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = '__all__'

class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'

class ComunicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicacao
        fields = '__all__'