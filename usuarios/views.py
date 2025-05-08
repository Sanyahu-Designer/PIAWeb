from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from clientes.models_profile import Profile
from clientes.models import Cliente
from .forms import UsuarioPrefeituraForm
from django.contrib import messages
from django.urls import reverse

# Apenas admin da prefeitura pode acessar

# Removi o import do UsuarioPrefeituraForm pois não está sendo usado nesta view.

def is_admin_prefeitura(user):
    # Permite acesso para admin da prefeitura ou superusuário
    return user.groups.filter(name='Admin da Prefeitura').exists() or user.is_superuser


def garantir_perfil_usuario(user, cliente):
    """Garante que o usuário tenha um perfil associado ao cliente correto.
    
    Esta função verifica se o usuário já tem um perfil. Se tiver e o cliente for diferente,
    atualiza o cliente. Se não tiver, cria um novo perfil.
    
    Args:
        user: O usuário para o qual garantir o perfil
        cliente: O cliente ao qual o perfil deve estar associado
    
    Returns:
        O perfil do usuário
    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Exclui qualquer perfil existente para evitar conflitos
    Profile.objects.filter(user=user).delete()
    
    # Cria um novo perfil com o cliente correto
    profile = Profile.objects.create(user=user, cliente=cliente)
    logger.debug(f"Perfil criado/atualizado para {user.username} no cliente {cliente.nome} (ID: {cliente.id})")
    
    return profile

@login_required
def usuarios_da_minha_prefeitura(request):
    # Se for superusuário no modo de impersonação, usa o cliente impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        cliente = request.impersonated_cliente
    else:
        # Verifica se é admin da prefeitura
        if not is_admin_prefeitura(request.user):
            return redirect('login')
        
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return render(request, 'usuarios/erro.html', {'mensagem': 'Seu usuário não está vinculado a uma prefeitura.'})
        cliente = profile.cliente
    
    # Busca todos os perfis associados a este cliente
    from clientes.models_profile import Profile
    perfis = Profile.objects.filter(cliente=cliente)
    
    # Obtém os IDs dos usuários associados a esses perfis
    user_ids = [perfil.user_id for perfil in perfis]
    
    # Busca os usuários completos, excluindo superusuários
    usuarios = User.objects.filter(id__in=user_ids, is_superuser=False).distinct()
    
    # Verifica se há usuários sem perfil associado ao cliente atual
    # Isso pode acontecer se um usuário foi criado mas o perfil não foi associado corretamente
    usuarios_sem_perfil = []
    
    # Registra no log para debug
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"Encontrados {usuarios.count()} usuários para o cliente {cliente.nome}")
    
    return render(request, 'usuarios/listar_usuarios_prefeitura.html', {
        'usuarios': usuarios, 
        'cliente': cliente,
        'usuarios_sem_perfil': usuarios_sem_perfil
    })

@login_required
def criar_usuario_prefeitura(request):
    # Se for superusuário no modo de impersonação, usa o cliente impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        cliente = request.impersonated_cliente
        # Registra para debug
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Superusuário impersonando cliente: {cliente.nome} (ID: {cliente.id})")
    else:
        # Verifica se é admin da prefeitura
        if not is_admin_prefeitura(request.user):
            return redirect('login')
        
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return render(request, 'usuarios/erro.html', {'mensagem': 'Seu usuário não está vinculado a uma prefeitura.'})
        cliente = profile.cliente
        # Registra para debug
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Admin usando cliente: {cliente.nome} (ID: {cliente.id})")
    
    if request.method == 'POST':
        form = UsuarioPrefeituraForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False
            
            # Grupos
            grupos = form.cleaned_data.get('grupos')
            if grupos:
                # Se o usuário pertence ao grupo 'Admin da Prefeitura', deve ter is_staff=True
                if grupos.filter(name='Admin da Prefeitura').exists():
                    user.is_staff = True
                else:
                    user.is_staff = False
            else:
                user.is_staff = False
            
            # Salva o usuário primeiro para obter um ID
            user.save()
            
            # Adiciona os grupos após salvar o usuário
            if grupos:
                user.groups.set(grupos)
            else:
                user.groups.clear()
            
            # Verifica se já existe um perfil para este usuário
            from clientes.models_profile import Profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'cliente': cliente}
            )
            
            # Se o perfil já existia mas estava associado a outro cliente, atualiza
            if not created and profile.cliente != cliente:
                profile.cliente = cliente
                profile.save()
                
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect(reverse('usuarios_minha_prefeitura'))
    else:
        form = UsuarioPrefeituraForm()
    return render(request, 'usuarios/criar_usuario_prefeitura.html', {'form': form, 'cliente': cliente})

@login_required
def editar_usuario_prefeitura(request, user_id):
    # Se for superusuário no modo de impersonação, usa o cliente impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        cliente = request.impersonated_cliente
        usuario = get_object_or_404(User, id=user_id, profile__cliente=cliente)
    else:
        # Verifica se é admin da prefeitura
        if not is_admin_prefeitura(request.user):
            return redirect('login')
        
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return render(request, 'usuarios/erro.html', {'mensagem': 'Seu usuário não está vinculado a uma prefeitura.'})
        
        cliente = profile.cliente
        usuario = get_object_or_404(User, id=user_id, profile__cliente=cliente)
    
    if request.method == 'POST':
        form = UsuarioPrefeituraForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False
            
            # Grupos
            grupos = form.cleaned_data.get('grupos')
            if grupos:
                # Se o usuário pertence ao grupo 'Admin da Prefeitura', deve ter is_staff=True
                if grupos.filter(name='Admin da Prefeitura').exists():
                    user.is_staff = True
                else:
                    user.is_staff = False
            else:
                user.is_staff = False
            
            # Salva o usuário primeiro
            user.save()
            
            # Adiciona os grupos após salvar o usuário
            if grupos:
                user.groups.set(grupos)
            else:
                user.groups.clear()
            
            # Verifica se já existe um perfil para este usuário
            from clientes.models_profile import Profile
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={'cliente': cliente}
            )
            
            # Se o perfil já existia mas estava associado a outro cliente, atualiza
            if not created and profile.cliente != cliente:
                profile.cliente = cliente
                profile.save()
                
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect(reverse('usuarios_minha_prefeitura'))
    else:
        form = UsuarioPrefeituraForm(instance=usuario)
    
    return render(request, 'usuarios/criar_usuario_prefeitura.html', {
        'form': form, 
        'cliente': cliente,
        'usuario': usuario,
        'modo_edicao': True
    })

@login_required
def excluir_usuario_prefeitura(request, user_id):
    # Se for superusuário no modo de impersonação, usa o cliente impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        cliente = request.impersonated_cliente
        usuario = get_object_or_404(User, id=user_id, profile__cliente=cliente)
    else:
        # Verifica se é admin da prefeitura
        if not is_admin_prefeitura(request.user):
            return redirect('login')
        
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return render(request, 'usuarios/erro.html', {'mensagem': 'Seu usuário não está vinculado a uma prefeitura.'})
        
        cliente = profile.cliente
        usuario = get_object_or_404(User, id=user_id, profile__cliente=cliente)
    
    # Não permitir excluir a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode excluir seu próprio usuário.')
        return redirect(reverse('usuarios_minha_prefeitura'))
    
    if request.method == 'POST':
        # Excluir o perfil primeiro para evitar problemas de integridade
        try:
            if hasattr(usuario, 'profile'):
                usuario.profile.delete()
            usuario.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao excluir usuário: {str(e)}')
        return redirect(reverse('usuarios_minha_prefeitura'))
    
    return render(request, 'usuarios/confirmar_exclusao.html', {'usuario': usuario, 'cliente': cliente})
