from clientes.models import Cliente
import logging
from django_multitenant.utils import set_current_tenant

logger = logging.getLogger(__name__)

class ImpersonationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se há uma sessão de impersonação ativa
        if request.user.is_authenticated and request.user.is_superuser:
            impersonated_cliente_id = request.session.get('impersonated_cliente_id')
            if impersonated_cliente_id:
                try:
                    cliente = Cliente.objects.get(id=impersonated_cliente_id)
                    # Log para debug (usando logger em vez de print)
                    logger.debug(f"Impersonando cliente: {cliente.id} - {cliente.nome}")
                    
                    request.is_impersonating = True
                    request.impersonated_cliente = cliente
                    
                    # Configurar o tenant atual para o django_multitenant
                    set_current_tenant(cliente)
                    
                    # Adicionar flags de permissão para superusuários
                    # Isso permite que eles usem as funcionalidades existentes de edição/exclusão
                    request.has_full_tenant_permissions = True
                    
                except Cliente.DoesNotExist:
                    # Se o cliente não existir mais, limpa a sessão
                    request.is_impersonating = False
                    if 'impersonated_cliente_id' in request.session:
                        del request.session['impersonated_cliente_id']
                    if 'impersonated_cliente_name' in request.session:
                        del request.session['impersonated_cliente_name']
                    # Garantir que nenhum tenant esteja configurado
                    set_current_tenant(None)
            else:
                request.is_impersonating = False
                # Garantir que nenhum tenant esteja configurado para superusuários sem impersonação
                set_current_tenant(None)
        else:
            request.is_impersonating = False

        response = self.get_response(request)
        return response
