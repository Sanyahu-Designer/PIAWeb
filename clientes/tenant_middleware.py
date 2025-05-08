from django_multitenant.utils import set_current_tenant
from clientes.models import Cliente
from clientes.models_profile import Profile
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
    """
    Middleware para configurar o tenant atual com base no usuário autenticado.
    Este middleware deve ser executado após o ImpersonationMiddleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Limpa qualquer tenant configurado anteriormente
        set_current_tenant(None)
        
        # Se o usuário já está em modo de impersonação, o tenant já foi configurado
        # pelo ImpersonationMiddleware, então não fazemos nada aqui
        if hasattr(request, 'is_impersonating') and request.is_impersonating:
            pass
        # Se o usuário está autenticado, mas não é superusuário e não está em modo de impersonação
        elif request.user.is_authenticated and not request.user.is_superuser:
            try:
                # Busca o profile do usuário para obter o cliente
                profile = Profile.objects.get(user=request.user)
                cliente = profile.cliente
                set_current_tenant(cliente)
                logger.debug(f"Tenant configurado para usuário: {cliente.id} - {cliente.nome}")
            except Profile.DoesNotExist:
                logger.warning(f"Usuário {request.user.username} não tem profile associado")
                set_current_tenant(None)
        # Se o usuário é superusuário sem impersonação, não configuramos nenhum tenant
        # (isso já foi feito no ImpersonationMiddleware)
        
        response = self.get_response(request)
        return response
