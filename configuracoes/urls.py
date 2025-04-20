from django.urls import path
from . import views

app_name = 'configuracoes'

urlpatterns = [
    # URL para redirecionar para a configuração existente ou para a página de criação
    path('', views.configuracao_redirect, name='configuracao_redirect'),
]
