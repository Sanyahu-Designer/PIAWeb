import logging

# Configurar o logger de auditoria
audit_logger = logging.getLogger('audit')

def log_data_access(request, model_name, object_id, action='view'):
    """
    Registra acesso a dados sensíveis no log de auditoria.
    
    Args:
        request: O objeto request do Django
        model_name: Nome do modelo acessado
        object_id: ID do objeto acessado
        action: Ação realizada (view, edit, delete, etc.)
    """
    # Obter informações do usuário
    username = request.user.username if request.user.is_authenticated else 'anonymous'
    
    # Obter informações do tenant
    tenant_info = "none"
    if hasattr(request, 'is_impersonating') and request.is_impersonating:
        tenant_info = f"{request.impersonated_cliente.id}:{request.impersonated_cliente.nome}"
    elif hasattr(request.user, 'profile') and request.user.profile and hasattr(request.user.profile, 'cliente'):
        tenant_info = f"{request.user.profile.cliente.id}:{request.user.profile.cliente.nome}"
    
    # Obter informações da requisição
    ip = get_client_ip(request)
    
    # Registrar o acesso
    audit_logger.info(
        f"action={action} model={model_name} id={object_id} "
        f"user={username} tenant={tenant_info} ip={ip} "
        f"impersonating={getattr(request, 'is_impersonating', False)}"
    )

def log_tenant_switch(request, old_tenant, new_tenant):
    """
    Registra mudança de tenant (impersonação) no log de auditoria.
    
    Args:
        request: O objeto request do Django
        old_tenant: Tenant anterior (pode ser None)
        new_tenant: Novo tenant
    """
    username = request.user.username if request.user.is_authenticated else 'anonymous'
    ip = get_client_ip(request)
    
    old_tenant_info = f"{old_tenant.id}:{old_tenant.nome}" if old_tenant else "none"
    new_tenant_info = f"{new_tenant.id}:{new_tenant.nome}" if new_tenant else "none"
    
    audit_logger.info(
        f"action=tenant_switch user={username} ip={ip} "
        f"old_tenant={old_tenant_info} new_tenant={new_tenant_info}"
    )

def get_client_ip(request):
    """
    Obtém o endereço IP do cliente, considerando proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
