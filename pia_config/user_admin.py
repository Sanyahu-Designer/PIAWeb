from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import path

# Personaliza o UserAdmin para usar o template do Material Dashboard 3
class CustomUserAdmin(UserAdmin):
    change_list_template = 'admin/auth/user/change_list_material_dashboard.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('perfil/', self.admin_site.admin_view(self.perfil_view), name='auth_user_perfil'),
        ]
        return custom_urls + urls
    
    def perfil_view(self, request):
        """
        View para exibir a página de perfil do usuário logado.
        """
        return render(request, 'admin/auth/user/perfil.html', {
            'title': 'Perfil do Usuário',
            'is_popup': False,
            'has_permission': True,
            'site_url': '/',
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
        })

# Desregistra o UserAdmin padrão e registra o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
