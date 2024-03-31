import logging
from django.shortcuts import render
from .serializer import (
    UserSerializer,
    EscolaSerializer,
    PerfilSerializer,
    EstudanteSerializer,
    IntegranteSerializer,
    PdiSerializer,
    ComunicacaoSerializer,
)
from .models import Arquivo, Escola, Perfil, Estudante, Integrante, Pdi, Comunicacao
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.urls import include, path
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView
from .forms import PdiForm, FormularioFormSet
from django.contrib.auth.decorators import login_required


log = logging.getLogger(__name__)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("list_students")
        else:
            return HttpResponse("Credenciais inválidas. Tente novamente.")
    return render(request, "login.html")


def list_students(request):
    log.info(request.user)
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        integrante = request.user.integrante_user.first()
        log.info(integrante)
        students = integrante.estudante_integrantes.all()
        log.info(students)
        return render(request, "estudantes.html", {"students": students})


def pdi_list(request, student_id):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        pdi_list = Pdi.objects.filter(estudante_id=student_id)
        student = Estudante.objects.get(id=student_id)
        return render(request, "pdi.html", {"pdi_list": pdi_list, "student": student})


def adicionar_pdi(request, estudante_id):
    if request.method == "POST":
        form = PdiForm(request.POST)
        formset = FormularioFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pdi = form.save(commit=False)
            pdi.estudante = Estudante.objects.get(pk=estudante_id)
            pdi.save()

            for form in formset:
                if form.cleaned_data:
                    formulario = form.save(commit=False)
                    formulario.pdi = pdi
                    formulario.save()

            habilidades = form.cleaned_data["habilidade"]
            competencias = form.cleaned_data["competencia"]
            log.info(competencias)
            if not isinstance(habilidades, list):
                habilidades = [habilidades]
            if not isinstance(competencias, list):
                competencias = [competencias]

            for habilidade in habilidades:
                pdi.habilidade.add(habilidade)

            for competencia in competencias:
                pdi.competencia.add(competencia)

            integrante = Integrante.objects.get(user=request.user)
            pdi.integrante.add(integrante)

            return redirect("pdi_list", student_id=estudante_id)
    else:
        form = PdiForm()
        formset = FormularioFormSet()
    return render(
        request,
        "add_pdi.html",
        {
            "form": form,
            "formset": formset,
            "estudante": Estudante.objects.get(pk=estudante_id),
        },
    )


#### APIS VIEWS #####


class EscolaViewSet(ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer([instance], many=True)
        return Response(serializer.data)

    def search(self, request):
        query_params = request.query_params
        nome = query_params.get("nome", "")
        endereco = query_params.get("endereco", "")
        localizacao = query_params.get("localacao", "")
        dep_adm = query_params.get("dep_adm", "")
        codigo_inep = query_params.get("codigo_inep", "")
        etapas = query_params.get("etapas", "")
        escolas = Escola.objects.filter(
            nome__icontains=nome,
            endereco__icontains=endereco,
            localizacao__icontains=localizacao,
            dep_adm__icontains=dep_adm,
            codigo_inep__icontains=codigo_inep,
            etapas__icontains=etapas,
        )
        serializer = EscolaSerializer(escolas, many=True)
        return Response(serializer.data)


class EstudanteViewSet(ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer


class PerfilViewSet(ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


class IntegranteViewSet(ModelViewSet):
    queryset = Integrante.objects.all()
    serializer_class = IntegranteSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PdiViewSet(ModelViewSet):
    queryset = Pdi.objects.all()
    serializer_class = PdiSerializer

    def create(self, request, *args, **kwargs):
        if request.data["data_inicial"] > request.data["data_final"]:
            return Response(self.kwargs, status=400)
        else:
            return super().create(request, *args, **kwargs)


class ComunicacaoViewSet(ModelViewSet):
    queryset = Comunicacao.objects.all()
    serializer_class = ComunicacaoSerializer
