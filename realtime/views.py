from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.contrib import messages as django_messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import PrivateMessage
from .forms import MessageForm
import logging
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)
User = get_user_model()

def ajax_login_required(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapped

@login_required
def user_autocomplete(request):
    """View para autocomplete de usuários no Select2"""
    term = request.GET.get('term', '')
    
    # Determinar o cliente atual (prefeitura)
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        # Se for superusuário impersonando, usa o cliente impersonado
        cliente = request.impersonated_cliente
    else:
        # Caso contrário, usa o cliente do perfil do usuário
        try:
            cliente = request.user.profile.cliente
        except Exception as e:
            logger.error(f"Erro ao obter cliente do usuário: {str(e)}")
            return JsonResponse({'results': [], 'pagination': {'more': False}})
    
    # Filtrar apenas usuários da mesma prefeitura
    users = User.objects.filter(profile__cliente=cliente).exclude(id=request.user.id)
    
    # Excluir superusuários da lista
    users = users.filter(is_superuser=False)
    
    # Aplicar filtro de busca se houver termo
    if term:
        users = users.filter(
            Q(username__icontains=term) |
            Q(first_name__icontains=term) |
            Q(last_name__icontains=term)
        )
    
    data = {
        'results': [{
            'id': str(user.id),
            'text': user.get_full_name() or user.username,
            'selected_text': user.get_full_name() or user.username
        } for user in users[:10]],
        'pagination': {'more': False}
    }
    
    return JsonResponse(data)

@ajax_login_required
def get_unread_count(request):
    try:
        unread_count = PrivateMessage.objects.filter(
            recipient=request.user,
            is_read=False,
            deleted_by_recipient=False
        ).count()
        return JsonResponse({'unread_count': unread_count, 'count': unread_count})
    except Exception as e:
        logger.error(f"Erro ao obter contagem de mensagens não lidas: {str(e)}")
        return JsonResponse({'error': 'Erro ao obter contagem'}, status=500)

@login_required
def chat_list(request):
    """Lista todas as mensagens do usuário (enviadas e recebidas) com paginação"""
    page = request.GET.get('page', 1)
    
    # Filtrar mensagens que não foram excluídas pelo usuário atual
    messages_list = PrivateMessage.objects.filter(
        (models.Q(sender=request.user) & models.Q(deleted_by_sender=False)) | 
        (models.Q(recipient=request.user) & models.Q(deleted_by_recipient=False))
    ).select_related('sender', 'recipient').order_by('-timestamp').distinct()
    
    paginator = Paginator(messages_list, 20)  # 20 mensagens por página
    try:
        chat_messages = paginator.page(page)
    except Exception:
        chat_messages = paginator.page(1)
    
    context = {
        'messages_list': chat_messages,
        'titulo': 'Mensagens',
        'unread_count': PrivateMessage.objects.filter(recipient=request.user, is_read=False, deleted_by_recipient=False).count()
    }
    
    return render(request, 'realtime/chat_list.html', context)

@login_required
def new_message(request):
    """Página para enviar uma nova mensagem"""
    # Obtém o destinatário da URL se fornecido
    recipient_id = request.GET.get('recipient')
    initial_data = {}
    
    if recipient_id:
        try:
            recipient = User.objects.get(id=recipient_id)
            initial_data['recipient'] = recipient
        except User.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = MessageForm(request.POST, sender=request.user, request=request)
        if form.is_valid():
            message = form.save()
            django_messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('realtime:chat_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    django_messages.error(request, f"{field}: {error}")
    else:
        form = MessageForm(initial=initial_data, sender=request.user, request=request)
    
    return render(request, 'realtime/new_message_form.html', {'form': form})

@login_required
def view_message(request, message_id):
    """Visualiza uma mensagem específica e marca como lida automaticamente"""
    message = get_object_or_404(PrivateMessage, id=message_id)
    
    if message.sender != request.user and message.recipient != request.user:
        return HttpResponseForbidden("Você não tem permissão para ver esta mensagem.")
    
    # Verifica se a mensagem foi excluída pelo usuário atual
    if message.is_deleted_for_user(request.user):
        django_messages.error(request, "Esta mensagem foi excluída.")
        return redirect('realtime:chat_list')
    
    try:
        with transaction.atomic():
            # Marca automaticamente como lida se o usuário for o destinatário
            if message.recipient == request.user and not message.is_read:
                message.is_read = True
                message.save(update_fields=['is_read'])
                
                # Atualiza o contador de mensagens não lidas via WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"notifications_{request.user.id}",
                    {
                        "type": "notification_message",
                        "message": "Mensagem marcada como lida",
                        "count": PrivateMessage.objects.filter(recipient=request.user, is_read=False, deleted_by_recipient=False).count()
                    }
                )
                
                # Dispara um evento para atualizar a interface
                if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                    return JsonResponse({
                        'status': 'ok',
                        'is_read': True,
                        'unread_count': PrivateMessage.objects.filter(recipient=request.user, is_read=False, deleted_by_recipient=False).count()
                    })
    except Exception as e:
        logger.error(f"Erro ao marcar mensagem como lida: {str(e)}")
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return JsonResponse({'error': 'Erro ao atualizar status'}, status=500)
    
    # Prepara o contexto para o template
    context = {
        'message': message,
        'is_recipient': message.recipient == request.user,
        'is_sender': message.sender == request.user,
        'unread_count': PrivateMessage.objects.filter(recipient=request.user, is_read=False).count()
    }
    
    return render(request, 'realtime/view_message.html', context)

@login_required
@require_POST
def toggle_read(request, message_id):
    """Marca/desmarca uma mensagem como lida"""
    try:
        with transaction.atomic():
            message = get_object_or_404(PrivateMessage, id=message_id, recipient=request.user)
            message.is_read = not message.is_read
            message.save(update_fields=['is_read'])
            return JsonResponse({
                'success': True,
                'is_read': message.is_read,
                'unread_count': PrivateMessage.objects.filter(recipient=request.user, is_read=False).count()
            })
    except Exception as e:
        logger.error(f"Erro ao alternar status de leitura: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Erro ao atualizar status'}, status=500)

@login_required
@require_POST
def delete_message(request, message_id):
    """Marca uma mensagem como excluída apenas para o usuário atual"""
    try:
        with transaction.atomic():
            message = get_object_or_404(PrivateMessage, id=message_id)
            
            if message.sender != request.user and message.recipient != request.user:
                return HttpResponseForbidden("Você não tem permissão para excluir esta mensagem.")
            
            # Em vez de excluir a mensagem, marca como excluída apenas para o usuário atual
            success = message.mark_as_deleted_for_user(request.user)
            
            if success:
                django_messages.success(request, 'Mensagem excluída com sucesso!')
            else:
                django_messages.error(request, 'Não foi possível excluir a mensagem.')
                
            return redirect('realtime:chat_list')
    except Exception as e:
        logger.error(f"Erro ao excluir mensagem: {str(e)}")
        django_messages.error(request, 'Erro ao excluir mensagem.')
        return redirect('realtime:chat_list')

@login_required
def get_notifications(request):
    """Retorna a lista de notificações não lidas do usuário"""
    from django.db.models import Q
    
    # Buscar mensagens não lidas e não excluídas
    notifications = PrivateMessage.objects.filter(
        Q(recipient=request.user),
        is_read=False,
        deleted_by_recipient=False
    ).order_by('-timestamp')[:5]
    
    # Formatar notificações
    notification_list = []
    for msg in notifications:
        sender_name = msg.sender.get_full_name() or msg.sender.username
        notification_list.append({
            'id': msg.id,
            'message_id': msg.id,  # ID da mensagem para redirecionamento
            'message': f'Nova mensagem de {sender_name}',
            'timestamp': msg.timestamp.isoformat(),
            'sender': sender_name,
            'is_read': msg.is_read
        })
    
    return JsonResponse({'notifications': notification_list})

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Marca uma notificação como lida"""
    try:
        message = get_object_or_404(PrivateMessage, id=notification_id, recipient=request.user)
        message.is_read = True
        message.save(update_fields=['is_read'])
        return JsonResponse({
            'success': True,
            'message_id': message.id  # Garantindo que o ID da mensagem seja retornado corretamente
        })
    except Exception as e:
        logger.error(f"Erro ao marcar notificação como lida: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def edit_message(request, message_id):
    """Edita uma mensagem existente"""
    message = get_object_or_404(PrivateMessage, id=message_id)
    
    # Verifica se o usuário tem permissão para editar a mensagem
    if message.sender != request.user and message.recipient != request.user:
        return HttpResponseForbidden("Você não tem permissão para editar esta mensagem.")
    
    # Apenas o remetente pode editar o conteúdo da mensagem
    is_sender = message.sender == request.user
    
    if request.method == 'POST' and is_sender:
        try:
            with transaction.atomic():
                # Atualiza a mensagem
                message_text = request.POST.get('message', '').strip()
                
                if not message_text:
                    raise ValidationError('A mensagem não pode estar vazia.')
                
                message.message = message_text
                message.save(update_fields=['message'])
                
                django_messages.success(request, 'Mensagem atualizada com sucesso!')
                return redirect('realtime:view_message', message_id=message.id)
                
        except ValidationError as e:
            logger.error(f"Erro de validação ao editar mensagem: {str(e)}")
            django_messages.error(request, str(e))
        except Exception as e:
            logger.error(f"Erro ao editar mensagem: {str(e)}", exc_info=True)
            django_messages.error(request, 'Ocorreu um erro ao editar a mensagem.')
    
    # Determinar o cliente atual (prefeitura)
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        # Se for superusuário impersonando, usa o cliente impersonado
        cliente = request.impersonated_cliente
    else:
        # Caso contrário, usa o cliente do perfil do usuário
        try:
            cliente = request.user.profile.cliente
        except Exception as e:
            logger.error(f"Erro ao obter cliente do usuário: {str(e)}")
            django_messages.error(request, 'Erro ao carregar usuários da prefeitura.')
            return redirect('realtime:chat_list')
    
    # Filtrar apenas usuários da mesma prefeitura
    users = User.objects.filter(profile__cliente=cliente).exclude(id=request.user.id)
    
    # Excluir superusuários da lista
    users = users.filter(is_superuser=False).order_by('first_name', 'last_name', 'username')
    
    context = {
        'message': message,
        'users': users,
        'is_sender': is_sender,
        'titulo': 'Editar Mensagem'
    }
    
    return render(request, 'realtime/edit_message.html', context)
