from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
import os
from django.conf import settings

# Create your views here.

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')(view_func))
    return decorated_view_func

@superuser_required
def auditoria_logs(request):
    # Auditoria do acesso à tela de logs
    from .audit import audit_log
    audit_log(
        action='view_audit_log',
        user=request.user,
        ip=request.META.get('REMOTE_ADDR'),
        objeto=None,
        old=None,
        new=None,
        result='success',
        extra=None
    )
    # Caminho do log de auditoria
    log_path = getattr(settings, 'AUDIT_LOG_PATH', os.path.join(settings.BASE_DIR, 'logs/audit.log'))
    logs = []
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            # Lê as últimas 200 linhas para evitar sobrecarga
            logs = f.readlines()[-200:]
    logs = [l.strip() for l in logs if l.strip()]
    return render(request, 'core/auditoria_logs.html', {'logs': logs})
