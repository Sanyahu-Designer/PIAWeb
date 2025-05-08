"""
Mixins para adicionar funcionalidades de permissões de superusuário às views.
"""
from django.contrib import messages
from django.shortcuts import redirect

class SuperuserPermissionsMixin:
    """
    Mixin que adiciona permissões especiais para superusuários quando estão no modo de impersonação.
    
    Este mixin deve ser usado em views que manipulam dados específicos de um cliente (tenant).
    Ele permite que superusuários possam editar, excluir e adicionar dados mesmo quando estão
    impersonando um cliente, enquanto usuários normais seguem as regras padrão de permissão.
    """
    
    def dispatch(self, request, *args, **kwargs):
        """
        Verifica se o usuário tem permissão para acessar a view.
        Superusuários em modo de impersonação têm permissões especiais.
        """
        # Verifica se o usuário é superusuário e está em modo de impersonação
        is_super_impersonating = (
            request.user.is_authenticated and 
            request.user.is_superuser and 
            hasattr(request, 'is_impersonating') and 
            request.is_impersonating
        )
        
        # Se for superusuário em modo de impersonação, adiciona flag à requisição
        if is_super_impersonating:
            request.has_tenant_edit_permission = True
            request.has_tenant_delete_permission = True
            
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Adiciona variáveis de contexto relacionadas a permissões de superusuário.
        """
        context = super().get_context_data(**kwargs)
        context['can_edit_tenant_data'] = getattr(self.request, 'has_tenant_edit_permission', False)
        context['can_delete_tenant_data'] = getattr(self.request, 'has_tenant_delete_permission', False)
        return context


class SuperuserCRUDMixin(SuperuserPermissionsMixin):
    """
    Mixin que estende o SuperuserPermissionsMixin para fornecer funcionalidades CRUD
    específicas para superusuários em modo de impersonação.
    
    Este mixin adiciona métodos auxiliares para verificar permissões e executar
    operações CRUD com mensagens apropriadas.
    """
    
    def can_edit(self):
        """Verifica se o usuário pode editar dados do tenant atual."""
        return getattr(self.request, 'has_tenant_edit_permission', False)
    
    def can_delete(self):
        """Verifica se o usuário pode excluir dados do tenant atual."""
        return getattr(self.request, 'has_tenant_delete_permission', False)
    
    def handle_no_permission(self):
        """Manipula o caso em que o usuário não tem permissão."""
        messages.error(self.request, "Você não tem permissão para realizar esta ação.")
        return redirect('dashboard')
    
    def form_valid(self, form):
        """
        Adiciona mensagem de sucesso personalizada para superusuários.
        """
        response = super().form_valid(form)
        if self.request.user.is_superuser and hasattr(self.request, 'is_impersonating'):
            cliente_nome = getattr(self.request, 'impersonated_cliente').nome
            if self.object.pk is None:  # Criação
                messages.success(
                    self.request, 
                    f"Registro criado com sucesso no cliente {cliente_nome}."
                )
            else:  # Edição
                messages.success(
                    self.request, 
                    f"Registro atualizado com sucesso no cliente {cliente_nome}."
                )
        return response
    
    def delete(self, request, *args, **kwargs):
        """
        Adiciona mensagem de sucesso personalizada para superusuários ao excluir.
        """
        if not self.can_delete():
            return self.handle_no_permission()
            
        cliente_nome = None
        if request.user.is_superuser and hasattr(request, 'is_impersonating'):
            cliente_nome = getattr(request, 'impersonated_cliente').nome
            
        response = super().delete(request, *args, **kwargs)
        
        if cliente_nome:
            messages.success(
                request, 
                f"Registro excluído com sucesso do cliente {cliente_nome}."
            )
            
        return response
