from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Remove o campo is_superuser se o usuário não for superusuário
        if self.user and not self.user.is_superuser:
            if 'is_superuser' in self.fields:
                del self.fields['is_superuser']

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 
                 'is_staff', 'is_superuser', 'groups', 'user_permissions')
