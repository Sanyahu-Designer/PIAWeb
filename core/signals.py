from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.core.signals import request_finished
from django.apps import apps
from .audit import audit_log

User = apps.get_model('auth', 'User')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    audit_log(
        action='login',
        user=user,
        ip=request.META.get('REMOTE_ADDR'),
        objeto=None,
        old=None,
        new=None,
        result='success',
        extra=None
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    audit_log(
        action='logout',
        user=user,
        ip=request.META.get('REMOTE_ADDR'),
        objeto=None,
        old=None,
        new=None,
        result='success',
        extra=None
    )

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    audit_log(
        action='login_failed',
        user=credentials.get('username'),
        ip=request.META.get('REMOTE_ADDR') if request else None,
        objeto=None,
        old=None,
        new=None,
        result='fail',
        extra=None
    )

# 1. Exclusão de dados pessoais
@receiver(pre_delete, sender=User)
def audit_user_delete(sender, instance, **kwargs):
    audit_log(
        action='delete',
        user=instance,
        ip=None,
        objeto=f'User:{instance.pk}',
        old=str(instance),
        new=None,
        result='success',
        extra=None
    )

# 2. Alteração de permissões, grupos e configurações sensíveis
@receiver(pre_save, sender=Group)
def audit_group_change(sender, instance, **kwargs):
    audit_log(
        action='change_group',
        user=None,
        ip=None,
        objeto=f'Group:{instance.pk}',
        old=None,
        new=str(instance),
        result='success',
        extra=None
    )

@receiver(pre_save, sender=Permission)
def audit_permission_change(sender, instance, **kwargs):
    audit_log(
        action='change_permission',
        user=None,
        ip=None,
        objeto=f'Permission:{instance.pk}',
        old=None,
        new=str(instance),
        result='success',
        extra=None
    )

# 3. Exportação/download de dados pessoais
# Sugestão: adicionar manualmente nas views de exportação (exemplo abaixo)
# from core.audit import audit_log
# audit_log(action='export', user=request.user, ip=request.META.get('REMOTE_ADDR'), objeto='Aluno:245', result='success')

# 4. Visualização de dados sensíveis
# Sugestão: adicionar manualmente nas views de detalhes sensíveis (exemplo abaixo)
# audit_log(action='view_sensitive', user=request.user, ip=request.META.get('REMOTE_ADDR'), objeto='Aluno:245', result='success')

# 5. Tentativas de acesso não autorizado já coberto
