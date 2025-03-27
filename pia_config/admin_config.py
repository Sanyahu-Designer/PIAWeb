from django.contrib import admin
from django.contrib.admin import AdminSite

# Configuração personalizada para o AdminSite
class MaterialDashboardAdminSite(AdminSite):
    # Sobrescreve os templates padrão do admin para usar os templates do Material Dashboard 3
    index_template = 'admin/index_material_dashboard.html'
    app_index_template = 'admin/app_index_material_dashboard.html'
    login_template = 'admin/login_material_dashboard.html'
    logout_template = 'admin/logout_material_dashboard.html'
    password_change_template = 'admin/password_change_material_dashboard.html'
    password_change_done_template = 'admin/password_change_done_material_dashboard.html'

# Substitui o site admin padrão pelo nosso site personalizado
admin_site = MaterialDashboardAdminSite(name='admin')

# Função para registrar um modelo com o template personalizado
def register_with_material_dashboard(model_or_iterable, admin_class=None, **options):
    """
    Registra um modelo com o template personalizado do Material Dashboard 3.
    """
    # Configura os templates personalizados
    if admin_class:
        admin_class.change_list_template = f'admin/{model_or_iterable._meta.app_label}/{model_or_iterable._meta.model_name}/change_list_material_dashboard.html'
        admin_class.change_form_template = f'admin/{model_or_iterable._meta.app_label}/{model_or_iterable._meta.model_name}/change_form_material_dashboard.html'
    
    # Registra o modelo no admin site
    return admin.register(model_or_iterable, admin_class, **options)
