from django import forms
from django.contrib.auth import get_user_model
from .models import PrivateMessage

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['recipient', 'message']
        widgets = {
            'recipient': forms.Select(attrs={
                'class': 'select2',
                'data-placeholder': 'Selecione um destinatário'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.sender:
            # Determinar o cliente atual (prefeitura)
            cliente = None
            
            # Se o usuário está impersonando, usa o cliente impersonado
            if self.request and hasattr(self.request, 'is_impersonating') and self.request.is_impersonating:
                cliente = self.request.impersonated_cliente
            # Caso contrário, usa o cliente do perfil do usuário
            elif hasattr(self.sender, 'profile') and hasattr(self.sender.profile, 'cliente'):
                cliente = self.sender.profile.cliente
            
            if cliente:
                # Filtra apenas usuários da mesma prefeitura
                recipient_queryset = User.objects.filter(profile__cliente=cliente).exclude(id=self.sender.id)
                
                # Excluir superusuários da lista
                recipient_queryset = recipient_queryset.filter(is_superuser=False)
            else:
                # Fallback para o comportamento anterior se não conseguir determinar o cliente
                recipient_queryset = User.objects.exclude(id=self.sender.id)
            
            # Configura o queryset e o label_from_instance para mostrar o nome completo
            self.fields['recipient'].queryset = recipient_queryset
            self.fields['recipient'].label_from_instance = self.get_user_full_name
        
        # Adiciona classes e estilos para melhorar a aparência
        self.fields['recipient'].label = 'Destinatário'
        self.fields['message'].label = 'Mensagem'
    
    def get_user_full_name(self, user):
        """Retorna o nome completo do usuário ou o nome de usuário se o nome completo não estiver disponível"""
        return user.get_full_name() or user.username
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.sender = self.sender
        instance.is_read = False
        
        # Obter o cliente atual
        # Se o usuário está impersonando um cliente, usa esse cliente
        request = getattr(self, 'request', None)
        if hasattr(self.sender, 'request'):
            request = self.sender.request
            
        if request and hasattr(request, 'is_impersonating') and request.is_impersonating:
            instance.cliente = request.impersonated_cliente
        elif hasattr(self.sender, 'profile') and hasattr(self.sender.profile, 'cliente'):
            # Usuário normal, usa o cliente do perfil
            instance.cliente = self.sender.profile.cliente
        
        if commit:
            instance.save()
        
        return instance