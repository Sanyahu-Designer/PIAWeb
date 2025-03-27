from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Personaliza o UserAdmin para usar o template do Material Dashboard 3
class CustomUserAdmin(UserAdmin):
    change_list_template = 'admin/auth/user/change_list_material_dashboard.html'

# Desregistra o UserAdmin padrão e registra o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
