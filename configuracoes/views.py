from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import ConfiguracaoCliente

# Create your views here.

@staff_member_required
def configuracao_redirect(request):
    """
    View que redireciona para a edição da configuração existente ou para a criação de uma nova,
    caso não exista nenhuma configuração.
    """
    # Verifica se já existe alguma configuração
    configuracao = ConfiguracaoCliente.objects.first()
    
    if configuracao:
        # Se existir, redireciona para a página de edição
        return redirect(f'/dashboard/admin/configuracoes/configuracaocliente/{configuracao.id}/change/')
    else:
        # Se não existir, redireciona para a página de criação
        return redirect('/dashboard/admin/configuracoes/configuracaocliente/add/')
