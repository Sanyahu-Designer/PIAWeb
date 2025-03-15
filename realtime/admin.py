from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from .models import PrivateMessage

User = get_user_model()

# Criamos uma classe de administração personalizada que redireciona todas as ações
@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'short_message', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read']
    search_fields = ['message']
    
    def get_model_perms(self, request):
        """
        Retorna permissões vazias para ocultar este modelo do índice do admin
        """
        return {}
    
    def changelist_view(self, request, extra_context=None):
        """Redireciona para a interface personalizada ao acessar a lista"""
        return redirect('realtime:chat_list')
    
    def response_change(self, request, obj):
        """Redireciona para a interface personalizada após salvar"""
        return redirect('realtime:view_message', message_id=obj.id)
    
    def response_add(self, request, obj, post_url_continue=None):
        """Redireciona para a interface personalizada após adicionar"""
        return redirect('realtime:view_message', message_id=obj.id)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """Redireciona para a interface personalizada ao acessar o formulário"""
        if object_id:
            return redirect('realtime:view_message', message_id=object_id)
        return redirect('realtime:new_message')
    
    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Mensagem'

# Re-registra o modelo User com o admin padrão do Django
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
