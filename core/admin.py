from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form_template = 'admin/auth/user/add_form.html'

    def get_fieldsets(self, request, obj=None):
        # Se for superusuário, mantém os fieldsets padrão
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        
        # Se estiver criando um novo usuário (obj=None)
        if obj is None:
            return (
                (None, {
                    'classes': ('wide',),
                    'fields': ('username', 'password1', 'password2'),
                }),
            )
        
        # Se estiver editando um usuário existente
        return [
            (None, {'fields': ('username', 'password')}),
            (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email')}),
            (_('Permissões'), {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
            (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
        ]

# Desregistra o admin padrão e registra o novo admin customizado para o User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)