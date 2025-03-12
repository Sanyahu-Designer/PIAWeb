from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from .models import PrivateMessage

User = get_user_model()

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'short_message', 'timestamp', 'is_read']
    list_filter = ['timestamp', 'is_read']
    search_fields = ['message']
    
    def get_fields(self, request, obj=None):
        if obj is None:  # Novo objeto
            return ['recipient', 'message']
        return ['sender', 'recipient', 'message', 'is_read', 'timestamp']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando
            return ['sender', 'timestamp']
        return []

    def save_model(self, request, obj, form, change):
        if not change:  # Nova mensagem
            obj.sender = request.user
            obj.is_read = False
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(models.Q(sender=request.user) | models.Q(recipient=request.user))
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recipient":
            kwargs["queryset"] = User.objects.exclude(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Mensagem'

# Re-registra o modelo User com o admin padrão do Django
from django.contrib.auth.admin import UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
