from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

@staff_member_required
def perfil_usuario(request):
    """
    View para exibir a página de perfil do usuário logado ou de um usuário específico.
    """
    # Verificar se foi passado um user_id na URL
    user_id = request.GET.get('user_id')
    
    if user_id:
        # Se foi passado um user_id, buscar o usuário correspondente
        user = get_object_or_404(User, id=user_id)
    else:
        # Caso contrário, usar o usuário logado
        user = request.user
        
    foto_url = None
    capa_url = None
    
    # Verificar se o usuário tem um profissional associado com foto
    try:
        if hasattr(user, 'profissional') and user.profissional.foto_perfil:
            foto_url = user.profissional.foto_perfil.url
    except:
        pass
    
    # Se não tiver profissional, verificar se tem foto no diretório padrão
    if not foto_url:
        foto_path = f'fotos_perfil/{user.username}.jpg'
        if default_storage.exists(foto_path):
            foto_url = default_storage.url(foto_path)
    
    # Verificar se o usuário tem uma imagem de capa
    capa_path = f'capas_perfil/{user.username}.jpg'
    if default_storage.exists(capa_path):
        capa_url = default_storage.url(capa_path)
    
    # Processar o upload da foto ou capa (apenas para o próprio usuário)
    if request.method == 'POST' and request.user.id == user.id:
        if request.FILES.get('foto_perfil'):
            foto = request.FILES['foto_perfil']
            try:
                if hasattr(user, 'profissional') and user.profissional:
                    user.profissional.foto_perfil = foto
                    user.profissional.save()
                    foto_url = user.profissional.foto_perfil.url
                else:
                    path = default_storage.save(f'fotos_perfil/{user.username}.jpg', ContentFile(foto.read()))
                    foto_url = default_storage.url(path)
            except Exception as e:
                messages.error(request, f'Erro ao salvar a foto: {str(e)}')
                path = default_storage.save(f'fotos_perfil/{user.username}.jpg', ContentFile(foto.read()))
                foto_url = default_storage.url(path)
            messages.success(request, 'Foto de perfil atualizada com sucesso!')
            return redirect('auth_user_perfil')
        elif request.FILES.get('capa_perfil'):
            capa = request.FILES['capa_perfil']
            if not capa.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                messages.error(request, 'A imagem de capa deve estar no formato JPG ou PNG.')
                return redirect('auth_user_perfil')
            if capa.size > 2 * 1024 * 1024:
                messages.error(request, 'A imagem de capa deve ter no máximo 2MB.')
                return redirect('auth_user_perfil')
            try:
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'capas_perfil'), exist_ok=True)
                path = default_storage.save(f'capas_perfil/{user.username}.jpg', ContentFile(capa.read()))
                capa_url = default_storage.url(path)
                messages.success(request, 'Imagem de capa atualizada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao salvar a imagem de capa: {str(e)}')
            return redirect('auth_user_perfil')
    
    return TemplateResponse(request, 'admin/auth/user/perfil.html', {
        'title': f'Perfil de {user.get_full_name() or user.username}',
        'foto_url': foto_url,
        'capa_url': capa_url,
        'profile_user': user,  # Passar o usuário do perfil para o template
        'is_own_profile': request.user.id == user.id,  # Indicar se é o próprio perfil do usuário
    })
