import logging
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import socket

# Configuração do logger de auditoria
AUDIT_LOG_PATH = getattr(settings, 'AUDIT_LOG_PATH', 'logs/audit.log')

# Função central de auditoria

def audit_log(action, user=None, ip=None, objeto=None, old=None, new=None, result=None, extra=None):
    """
    Registra uma linha de auditoria no formato LGPD-compliant.
    Parâmetros:
        action: string (ex: 'create', 'update', 'delete', 'login', 'logout', 'tenant_switch', etc)
        user: User instance ou string identificando o usuário
        ip: string IP de origem
        objeto: string identificando o objeto afetado (ex: 'Aluno:245')
        old: valor anterior (quando aplicável)
        new: valor novo (quando aplicável)
        result: 'success', 'fail', etc
        extra: dict ou string com informações adicionais
    """
    if hasattr(user, 'pk'):
        user_id = user.pk
        user_name = getattr(user, 'username', str(user))
    elif isinstance(user, str):
        user_id = ''
        user_name = user
    else:
        user_id = ''
        user_name = ''

    if ip is None and hasattr(user, 'last_login'):
        try:
            ip = user.last_login_ip
        except Exception:
            pass
    timestamp = now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
    ip = ip or 'unknown'
    parts = [
        f"AUDIT {timestamp}",
        f"action={action}",
        f"user={user_name}",
        f"user_id={user_id}",
        f"ip={ip}"
    ]
    if objeto:
        parts.append(f"objeto={objeto}")
    if old is not None:
        parts.append(f"old={old}")
    if new is not None:
        parts.append(f"new={new}")
    if result is not None:
        parts.append(f"result={result}")
    if extra:
        if isinstance(extra, dict):
            for k, v in extra.items():
                parts.append(f"{k}={v}")
        else:
            parts.append(f"extra={extra}")
    line = ' '.join(parts)
    try:
        with open(AUDIT_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception as e:
        logging.error(f"Erro ao registrar auditoria: {e}")
