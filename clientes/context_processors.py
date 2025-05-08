"""
Context processors para adicionar informações de superusuário e permissões ao contexto de templates.
"""

def superuser_permissions(request):
    """
    Adiciona variáveis de contexto relacionadas a permissões de superusuário.
    
    Este context processor adiciona as seguintes variáveis ao contexto:
    - is_superuser: Indica se o usuário atual é um superusuário
    - can_edit_tenant_data: Indica se o usuário pode editar dados do tenant atual
    - can_delete_tenant_data: Indica se o usuário pode excluir dados do tenant atual
    - current_tenant: O tenant atual (Cliente) que está sendo impersonado
    """
    context = {
        'is_superuser': request.user.is_superuser if request.user.is_authenticated else False,
        'can_edit_tenant_data': False,
        'can_delete_tenant_data': False,
        'current_tenant': None,
    }
    
    # Se o usuário é superusuário e está impersonando um cliente
    if request.user.is_authenticated and request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        context['can_edit_tenant_data'] = True
        context['can_delete_tenant_data'] = True
        context['current_tenant'] = request.impersonated_cliente
    
    return context
