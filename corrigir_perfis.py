#!/usr/bin/env python
"""
Script para corrigir perfis de usuários que estão associados ao cliente errado.
Este script deve ser executado usando o shell do Django:
    python manage.py shell < corrigir_perfis.py
"""

import os
import django
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar modelos
from django.contrib.auth.models import User
from clientes.models_profile import Profile
from clientes.models import Cliente

# Listar todos os clientes
clientes = Cliente.objects.all()
logger.info(f"Total de clientes: {clientes.count()}")
for cliente in clientes:
    logger.info(f"Cliente ID: {cliente.id}, Nome: {cliente.nome}")

# Listar todos os usuários e seus perfis
users = User.objects.all()
logger.info(f"Total de usuários: {users.count()}")

for user in users:
    try:
        profile = Profile.objects.get(user=user)
        logger.info(f"Usuário: {user.username}, ID: {user.id}, Cliente: {profile.cliente.nome}, Cliente ID: {profile.cliente.id}")
    except Profile.DoesNotExist:
        logger.info(f"Usuário: {user.username}, ID: {user.id}, SEM PERFIL")
    except Profile.MultipleObjectsReturned:
        profiles = Profile.objects.filter(user=user)
        logger.info(f"Usuário: {user.username}, ID: {user.id}, MÚLTIPLOS PERFIS:")
        for p in profiles:
            logger.info(f"  - Perfil ID: {p.id}, Cliente: {p.cliente.nome}, Cliente ID: {p.cliente.id}")

# Corrigir usuários com múltiplos perfis
users_with_multiple_profiles = []
for user in users:
    if Profile.objects.filter(user=user).count() > 1:
        users_with_multiple_profiles.append(user)

logger.info(f"Usuários com múltiplos perfis: {len(users_with_multiple_profiles)}")
for user in users_with_multiple_profiles:
    profiles = Profile.objects.filter(user=user)
    logger.info(f"Corrigindo perfis para {user.username}:")
    
    # Manter apenas o perfil mais recente
    latest_profile = profiles.latest('id')
    logger.info(f"  - Mantendo perfil ID: {latest_profile.id}, Cliente: {latest_profile.cliente.nome}")
    
    # Excluir outros perfis
    for profile in profiles:
        if profile.id != latest_profile.id:
            logger.info(f"  - Excluindo perfil ID: {profile.id}, Cliente: {profile.cliente.nome}")
            profile.delete()

# Corrigir usuários sem perfil
users_without_profile = []
for user in users:
    if not Profile.objects.filter(user=user).exists():
        users_without_profile.append(user)

logger.info(f"Usuários sem perfil: {len(users_without_profile)}")
if users_without_profile:
    # Usar o primeiro cliente como padrão
    default_cliente = Cliente.objects.first()
    logger.info(f"Usando cliente padrão: {default_cliente.nome}, ID: {default_cliente.id}")
    
    for user in users_without_profile:
        logger.info(f"Criando perfil para {user.username} com cliente {default_cliente.nome}")
        Profile.objects.create(user=user, cliente=default_cliente)

logger.info("Correção concluída!")
