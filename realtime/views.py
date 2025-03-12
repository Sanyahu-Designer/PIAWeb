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
from .models import PrivateMessage
import logging

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
    
    users = User.objects.exclude(id=request.user.id)
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
            is_read=False
        ).count()
        return JsonResponse({'unread_count': unread_count})
    except Exception as e:
        logger.error(f"Erro ao obter contagem de mensagens não lidas: {str(e)}")
        return JsonResponse({'error': 'Erro ao obter contagem'}, status=500)

@login_required
def chat_list(request):
    """Lista todas as mensagens do usuário (enviadas e recebidas) com paginação"""
    page = request.GET.get('page', 1)
    messages_list = PrivateMessage.objects.filter(
        models.Q(sender=request.user) | models.Q(recipient=request.user)
    ).select_related('sender', 'recipient').order_by('-timestamp').distinct()
    
    paginator = Paginator(messages_list, 20)  # 20 mensagens por página
    try:
        chat_messages = paginator.page(page)
    except Exception:
        chat_messages = paginator.page(1)
    
    context = {
        'messages_list': chat_messages,
        'titulo': 'Mensagens',
        'unread_count': PrivateMessage.objects.filter(recipient=request.user, is_read=False).count()
    }
    
    return render(request, 'realtime/chat_list.html', context)

@login_required
def new_message(request):
    """Página para enviar uma nova mensagem"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        message_text = request.POST.get('message', '').strip()
        
        try:
            # Adiciona logs para debug
            logger.info(f"Tentando criar nova mensagem. User: {request.user}, Auth: {request.user.is_authenticated}")
            
            if not request.user.is_authenticated:
                raise ValidationError('Usuário não está autenticado.')
                
            if not recipient_id or not message_text:
                raise ValidationError('Por favor, selecione um destinatário e digite uma mensagem.')
            
            recipient = get_object_or_404(User, id=recipient_id)
            
            if recipient == request.user:
                raise ValidationError('Você não pode enviar mensagem para si mesmo.')
            
            # Verifica se o usuário existe antes de criar a mensagem
            if not User.objects.filter(id=request.user.id).exists():
                raise ValidationError('Usuário remetente não encontrado no banco de dados.')
            
            message = PrivateMessage(
                sender=request.user,
                recipient=recipient,
                message=message_text
            )
            
            # Adiciona log antes de salvar
            logger.info(f"Criando mensagem. Sender: {message.sender}, Recipient: {message.recipient}")
            
            message.full_clean()
            message.save()
            
            django_messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('realtime:chat_list')
            
        except ValidationError as e:
            logger.error(f"Erro de validação ao criar mensagem: {str(e)}")
            django_messages.error(request, str(e))
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}", exc_info=True)
            django_messages.error(request, 'Ocorreu um erro ao enviar a mensagem.')
    
    # Obtém o destinatário da URL se fornecido
    recipient_id = request.GET.get('recipient')
    recipient = None
    
    if recipient_id:
        try:
            recipient = User.objects.get(id=recipient_id)
        except (User.DoesNotExist, ValueError):
            pass
    
    # Lista todos os usuários exceto o atual
    users = User.objects.exclude(id=request.user.id).order_by('first_name', 'last_name', 'username')
    
    context = {
        'users': users,
        'recipient': recipient
    }
    
    return render(request, 'realtime/new_message.html', context)

@login_required
def view_message(request, message_id):
    """Visualiza uma mensagem específica e marca como lida automaticamente"""
    message = get_object_or_404(PrivateMessage, id=message_id)
    
    if message.sender != request.user and message.recipient != request.user:
        return HttpResponseForbidden("Você não tem permissão para ver esta mensagem.")
    
    try:
        with transaction.atomic():
            if message.recipient == request.user and not message.is_read:
                message.is_read = True
                message.save(update_fields=['is_read'])
                
                if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                    return JsonResponse({'status': 'ok', 'is_read': True})
    except Exception as e:
        logger.error(f"Erro ao marcar mensagem como lida: {str(e)}")
        if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
            return JsonResponse({'error': 'Erro ao atualizar status'}, status=500)
    
    return render(request, 'realtime/view_message.html', {'message': message})

@login_required
@require_POST
def toggle_read(request, message_id):
    """Marca/desmarca uma mensagem como lida"""
    try:
        with transaction.atomic():
            message = get_object_or_404(PrivateMessage, id=message_id, recipient=request.user)
            message.is_read = not message.is_read
            message.save(update_fields=['is_read'])
            return JsonResponse({'is_read': message.is_read})
    except Exception as e:
        logger.error(f"Erro ao alternar status de leitura: {str(e)}")
        return JsonResponse({'error': 'Erro ao atualizar status'}, status=500)

@login_required
@require_POST
def delete_message(request, message_id):
    """Exclui uma mensagem"""
    try:
        with transaction.atomic():
            message = get_object_or_404(PrivateMessage, id=message_id)
            
            if message.sender != request.user and message.recipient != request.user:
                return HttpResponseForbidden("Você não tem permissão para excluir esta mensagem.")
            
            message.delete()
            django_messages.success(request, 'Mensagem excluída com sucesso!')
            return redirect('realtime:chat_list')
    except Exception as e:
        logger.error(f"Erro ao excluir mensagem: {str(e)}")
        django_messages.error(request, 'Erro ao excluir mensagem.')
        return redirect('realtime:chat_list')

@login_required
def get_notifications(request):
    """Retorna a lista de notificações não lidas do usuário"""
    from django.db.models import Q
    
    # Buscar mensagens não lidas
    notifications = PrivateMessage.objects.filter(
        Q(recipient=request.user),
        is_read=False
    ).order_by('-timestamp')[:5]
    
    # Formatar notificações
    notification_list = []
    for msg in notifications:
        notification_list.append({
            'id': msg.id,
            'message': f'Nova mensagem de {msg.sender.get_full_name() or msg.sender.username}',
            'timestamp': msg.timestamp.isoformat()
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
        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Erro ao marcar notificação como lida: {str(e)}")
        return JsonResponse({'status': 'error'}, status=500)
