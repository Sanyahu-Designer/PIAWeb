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
        super().__init__(*args, **kwargs)
        
        if self.sender:
            # Filtra os usuários excluindo o remetente
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
        
        if commit:
            instance.save()
        
        return instance 