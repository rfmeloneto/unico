import logging
from collections import defaultdict
import json
from datetime import date
from django.db.models import Sum, Count, Q, F, Avg
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from .serializer import (
    UserSerializer,
    EscolaSerializer,
    PerfilSerializer,
    EstudanteSerializer,
    IntegranteSerializer,
    PdiSerializer,
    ComunicacaoSerializer,
)
from .models import (
    Arquivo,
    Escola,
    Perfil,
    Estudante,
    Integrante,
    Pdi,
    Comunicacao,
    Formulario,
    Avaliacao,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.views import Response
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from rest_framework.decorators import api_view
from django.urls import include, path, reverse
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import UpdateView
from .forms import PdiForm, FormularioForm, ComunicacaoForm, AvaliacaoForm, PdiEditForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse


log = logging.getLogger(__name__)


from django.http import JsonResponse


def delete_pdi(request, pdi_id):
    pdi = get_object_or_404(Pdi, pk=pdi_id)
    estudante = pdi.estudante.id
    if request.method == "POST":
        pdi.delete()
        messages.success(request, "O PDI foi excluído com sucesso.")
        return JsonResponse(
            {"redirect": reverse("pdi_list", kwargs={"student_id": estudante})}
        )
    return JsonResponse({"error": "Método não permitido."}, status=405)


def delete_atividade(request, atividade_id):
    atividade = get_object_or_404(Formulario, pk=atividade_id)
    pdi_id = atividade.pdi_id
    if request.method == "POST":
        atividade.delete()
        messages.success(request, "A atividade foi excluída com sucesso.")
        return JsonResponse(
            {"redirect": request.path}
        )  # Redirecionar de volta para a mesma página
    return JsonResponse({"error": "Método não permitido."}, status=405)


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
        if form.is_valid():
            pdi = form.save(commit=False)
            pdi.estudante = Estudante.objects.get(pk=estudante_id)
            pdi.save()
            if form.cleaned_data:
                formulario = form.save(commit=False)
                formulario.pdi = pdi
                formulario.save()
            integrante = Integrante.objects.get(user=request.user)
            pdi.integrante.add(integrante)

            return redirect("pdi_list", student_id=estudante_id)
    else:
        form = PdiForm()
    return render(
        request,
        "add_pdi.html",
        {
            "form": form,
            "estudante": Estudante.objects.get(pk=estudante_id),
        },
    )


def edit_pdi(request, pdi_id):
    pdi = Pdi.objects.get(pk=pdi_id)
    comentarios = Comunicacao.objects.filter(pdi__id=pdi_id)
    estudante = pdi.estudante
    atividades = Formulario.objects.filter(pdi__id=pdi_id)
    arquivos = Arquivo.objects.filter(pdi_arquivo__id=pdi_id)
    avaliacoes = Avaliacao.objects.filter(pdi__id=pdi_id)
    if request.method == "POST":
        form = PdiEditForm(request.POST, instance=pdi)
        if form.is_valid():
            form.save()
            arquivo_enviado = request.FILES.get("arquivo")
            if arquivo_enviado:
                arquivo = Arquivo.objects.create(
                    titulo=arquivo_enviado.name, file=arquivo_enviado
                )
                pdi.arquivo = arquivo
            pdi.save()
            return redirect("pdi_list", student_id=pdi.estudante_id)
    else:
        form = PdiEditForm(instance=pdi)
    return render(
        request,
        "edit_pdi.html",
        {
            "avaliacoes": avaliacoes,
            "form": form,
            "pdi": pdi,
            "estudante": estudante,
            "atividades": atividades,
            "comentarios": comentarios,
            "arquivos": arquivos,
        },
    )


def add_activites(request, pdi_id):
    form = FormularioForm()
    if request.method == "POST":
        form = FormularioForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            pdi = Pdi.objects.get(pk=pdi_id)
            formulario.pdi = pdi
            formulario.save()
            return redirect("edit_pdi", pdi_id=pdi.id)
    return render(
        request,
        "add_activites.html",
        {
            "pdi_id": Pdi.objects.get(pk=pdi_id),
            "form": form,
        },
    )


def edit_activites(request, atividade_id):
    atividade = Formulario.objects.get(pk=atividade_id)
    if request.method == "POST":
        form = FormularioForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect("edit_pdi", pdi_id=atividade.pdi.id)
    else:
        form = FormularioForm(instance=atividade)
    return render(
        request,
        "edit_activites.html",
        {
            "pdi_id": atividade.pdi,
            "form": form,
        },
    )


def add_comentario(request, pdi_id):
    form = ComunicacaoForm()
    user = request.user.integrante_user.first()
    arquivos = Arquivo.objects.filter(comunicacao_arquivo__id=pdi_id)
    if request.method == "POST":
        form = ComunicacaoForm(request.POST)
        if form.is_valid():
            comunicacao = form.save(commit=False)
            pdi = Pdi.objects.get(pk=pdi_id)
            arquivo_enviado = request.FILES.get("arquivo")
            if arquivo_enviado:
                arquivo = Arquivo.objects.create(
                    titulo=arquivo_enviado.name, file=arquivo_enviado
                )
                comunicacao.arquivo = arquivo
            comunicacao.pdi = pdi
            comunicacao.autor = user
            comunicacao.save()
            return redirect("edit_pdi", pdi_id=pdi_id)
    return render(
        request,
        "add_comentario.html",
        {
            "arquivos_comunicacao": arquivos,
            "pdi_id": Pdi.objects.get(pk=pdi_id),
            "form": form,
        },
    )


def download_files(request, arquivo_id):
    arquivo = Arquivo.objects.get(pk=arquivo_id)
    file_path = arquivo.file.path
    file_name = arquivo.file.name.split("/")[-1]

    try:
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=file_name
        )
    except FileNotFoundError:
        raise Http404("Arquivo não encontrado")


def avaliar_pdi(request, pdi_id):
    pdi = get_object_or_404(Pdi, pk=pdi_id)
    if request.method == "POST":
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.pdi = pdi
            avaliacao.nota = form.cleaned_data["nota"]
            avaliacao.save()
            # return redirect("pdi_list", student_id=pdi.estudante_id)
            return redirect("edit_pdi", pdi_id=pdi.id)
    else:
        form = AvaliacaoForm()
    return render(
        request,
        "avaliar_pdi.html",
        {
            "pdi_id": pdi,
            "form": form,
        },
    )


def development_panel(request, estudante_id):
    estudante = get_object_or_404(Estudante, pk=estudante_id)
    pdis = Pdi.objects.filter(estudante=estudante_id)
    avaliacoes = Avaliacao.objects.filter(pdi__estudante=estudante_id)
    atividades = Formulario.objects.filter(pdi__estudante=estudante_id)
    average_notas_por_habilidade = Formulario.objects.values(
        "habilidade__habilidade"
    ).annotate(avg_nota=Avg("nota"))
    media_habilidades = {
        item["habilidade__habilidade"]: item["avg_nota"]
        for item in average_notas_por_habilidade
    }

    media_geral = Avaliacao.objects.aggregate(Avg("nota"))["nota__avg"] or 0

    total_pdis = Pdi.objects.filter(estudante=estudante_id).count()

    total_pdis_abertos = Pdi.objects.filter(estudante=estudante_id, concluido=False)
    total_pdis_concluidos = Pdi.objects.filter(estudante=estudante_id, concluido=True)

    pdi_avaliacao = Avaliacao.objects.filter(pdi__estudante=estudante_id)

    nota_counts = defaultdict(int)

    for avaliacao in pdi_avaliacao:
        nota = avaliacao.get_nota_display()
        nota_counts[nota] += 1

    return render(
        request,
        "development_panel.html",
        {
            "nota_counts": nota_counts,
            "total_pdis_concluidos": total_pdis_concluidos,
            "total_pdis_abertos": total_pdis_abertos,
            "total_pdis": total_pdis,
            "media_geral": media_geral,
            "media_habilidades": media_habilidades,
            "estudante": estudante,
            "pdis": pdis,
            "avaliacoes": avaliacoes,
            "atividades": atividades,
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
