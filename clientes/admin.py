from django.contrib import admin
from .models import Cliente
from .models_profile import Profile

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cnpj", "slug")  # Removido o campo dominio
    search_fields = ("nome", "cnpj", "slug")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "cliente")
    search_fields = ("user__username", "cliente__nome")
