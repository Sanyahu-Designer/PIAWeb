from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Personaliza o UserAdmin para usar o template do Material Dashboard 3
class CustomUserAdmin(UserAdmin):
    # Mantém as configurações padrão do UserAdmin
    pass

# Desregistra o UserAdmin padrão e registra o nosso personalizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
