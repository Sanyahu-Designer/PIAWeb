from django.urls import path
from .views import (
    nova_prefeitura, listar_clientes, ver_cliente, excluir_cliente, 
    editar_cliente, listar_usuarios_cliente, confirmar_excluir_cliente,
    impersonate_cliente, stop_impersonation
)

urlpatterns = [
    path('nova/', nova_prefeitura, name='nova_prefeitura'),
    path('listar/', listar_clientes, name='listar_clientes'),
    path('ver/<int:cliente_id>/', ver_cliente, name='ver_cliente'),
    path('confirmar-excluir/<int:cliente_id>/', confirmar_excluir_cliente, name='confirmar_excluir_cliente'),
    path('excluir/<int:cliente_id>/', excluir_cliente, name='excluir_cliente'),
    path('editar/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('usuarios/<int:cliente_id>/', listar_usuarios_cliente, name='listar_usuarios_cliente'),
    path('impersonate/<int:cliente_id>/', impersonate_cliente, name='impersonate_cliente'),
    path('stop-impersonation/', stop_impersonation, name='stop_impersonation'),
]
