# forms.py

from django import forms
from django.contrib.auth.models import User, Group

class UsuarioPrefeituraForm(forms.ModelForm):
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput, required=True)
    grupos = forms.ModelMultipleChoiceField(
        label='Grupos',
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'style': 'width: 100%;'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupos'].queryset = Group.objects.all()
        
        # Remover password e password_confirm dos campos obrigatórios apenas para edição
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        # Para um novo usuário, a senha é obrigatória
        if not self.instance.pk and not password:
            self.add_error('password', 'Este campo é obrigatório para novos usuários.')
        
        # Verificar se as senhas coincidem apenas se pelo menos uma foi fornecida
        if password or password_confirm:
            if password != password_confirm:
                raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
