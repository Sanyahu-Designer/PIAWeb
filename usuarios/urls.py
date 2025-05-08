from django.urls import path
from .views import usuarios_da_minha_prefeitura, criar_usuario_prefeitura, editar_usuario_prefeitura, excluir_usuario_prefeitura

urlpatterns = [
    path('', usuarios_da_minha_prefeitura, name='usuarios_minha_prefeitura'),
    path('novo/', criar_usuario_prefeitura, name='criar_usuario_prefeitura'),
    path('editar/<int:user_id>/', editar_usuario_prefeitura, name='editar_usuario_prefeitura'),
    path('excluir/<int:user_id>/', excluir_usuario_prefeitura, name='excluir_usuario_prefeitura'),
]
