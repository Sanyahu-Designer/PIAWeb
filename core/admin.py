from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm
from django.apps import apps

# Alterar o nome da aplicação auth para 'Usuários'
auth_app = apps.get_app_config('auth')
auth_app.verbose_name = 'Usuários'

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    change_form_template = 'admin/change_form_standard.html'
    add_form_template = 'admin/change_form_standard.html'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Passa o usuário atual para o formulário
        if hasattr(form, 'user'):
            form.user = request.user
        if not request.user.is_superuser:
            if 'is_superuser' in form.base_fields:
                del form.base_fields['is_superuser']
        return form

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