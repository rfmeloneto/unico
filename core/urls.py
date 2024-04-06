from rest_framework import routers, serializers, viewsets
from django.urls import include, path
from .views import (
    PdiViewSet,
    ComunicacaoViewSet,
    IntegranteViewSet,
    EscolaViewSet,
    EstudanteViewSet,
    PerfilViewSet,
    UserViewSet,
    login_view,
    list_students,
    pdi_list,
    adicionar_pdi,
    add_activites,
    edit_pdi,
    delete_atividade,
    delete_pdi,
    edit_activites,
)


urlpatterns = [
    path("", login_view, name="login"),
    path("lista-estudantes", list_students, name="list_students"),
    path("pdi_list/<int:student_id>/", pdi_list, name="pdi_list"),
    path("add_pdi/<int:estudante_id>/", adicionar_pdi, name="add_pdi"),
    path("add_activites/<int:pdi_id>/", add_activites, name="add_activites"),
    path("edit_pdi/<int:pdi_id>/", edit_pdi, name="edit_pdi"),
    path("delete_pdi/<int:pdi_id>/", delete_pdi, name="delete_pdi"),
    path(
        "delete_atividade/<int:atividade_id>/",
        delete_atividade,
        name="delete_atividade",
    ),
    path("edit_activites/<int:atividade_id>/", edit_activites, name="edit_activites"),
    ### API URLS ###
    path(
        "v1/escola/<int:pk>/",
        EscolaViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
                "get": "search",
            }
        ),
    ),
    path("v1/escola/<str:text>/", EscolaViewSet.as_view({"get": "search"})),
    path("v1/escola/", EscolaViewSet.as_view({"post": "create", "get": "list"})),
    path(
        "v1/estudante/<int:pk>/",
        EstudanteViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
    path("v1/estudante/", EstudanteViewSet.as_view({"post": "create", "get": "list"})),
    path(
        "v1/perfil/<int:pk>/",
        PerfilViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
    path("v1/perfil/", PerfilViewSet.as_view({"post": "create", "get": "list"})),
    path(
        "v1/integrantes/<int:pk>/",
        IntegranteViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
    path(
        "v1/integrantes/", IntegranteViewSet.as_view({"post": "create", "get": "list"})
    ),
    path("v1/user/", UserViewSet.as_view({"post": "create", "get": "list"})),
    path(
        "v1/user/<int:pk>/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
    path("v1/pdi/", PdiViewSet.as_view({"post": "create", "get": "list"})),
    path(
        "v1/pdi/<int:pk>/",
        PdiViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
    path(
        "v1/comunicacao/", ComunicacaoViewSet.as_view({"post": "create", "get": "list"})
    ),
    path(
        "v1/comunicacao/<int:pk>/",
        ComunicacaoViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
                "patch": "partial_update",
            }
        ),
    ),
]
