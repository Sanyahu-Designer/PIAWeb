#!/usr/bin/env python
"""
Script para corrigir perfis de usuários que estão associados ao cliente errado.
Este script deve ser executado usando o shell do Django:
    python manage.py shell < fix_user_profiles.py
"""

import sys
import logging
from django.contrib.auth.models import User
from clientes.models_profile import Profile
from clientes.models import Cliente

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_user_profiles():
    """Corrige perfis de usuários que estão associados ao cliente errado."""
    logger.info("Iniciando correção de perfis de usuários...")
    
    # Obter todos os usuários
    users = User.objects.all()
    logger.info(f"Total de usuários: {users.count()}")
    
    # Obter todos os perfis
    profiles = Profile.objects.all()
    logger.info(f"Total de perfis: {profiles.count()}")
    
    # Verificar usuários sem perfil
    users_without_profile = []
    for user in users:
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            users_without_profile.append(user)
    
    logger.info(f"Usuários sem perfil: {len(users_without_profile)}")
    for user in users_without_profile:
        logger.info(f"  - {user.username} (ID: {user.id})")
    
    # Verificar perfis duplicados
    user_ids_with_multiple_profiles = []
    for user in users:
        profile_count = Profile.objects.filter(user=user).count()
        if profile_count > 1:
            user_ids_with_multiple_profiles.append(user.id)
    
    logger.info(f"Usuários com múltiplos perfis: {len(user_ids_with_multiple_profiles)}")
    for user_id in user_ids_with_multiple_profiles:
        user = User.objects.get(id=user_id)
        profiles = Profile.objects.filter(user=user)
        logger.info(f"  - {user.username} (ID: {user.id}) tem {profiles.count()} perfis:")
        for profile in profiles:
            logger.info(f"    - Perfil ID: {profile.id}, Cliente: {profile.cliente.nome} (ID: {profile.cliente.id})")
    
    # Perguntar se deseja corrigir os problemas
    if users_without_profile or user_ids_with_multiple_profiles:
        logger.info("Problemas encontrados. Deseja corrigir? (s/n)")
        
        # Como estamos em um script, vamos assumir que sim
        choice = 's'
        
        if choice.lower() == 's':
            # Corrigir usuários com múltiplos perfis
            for user_id in user_ids_with_multiple_profiles:
                user = User.objects.get(id=user_id)
                profiles = Profile.objects.filter(user=user)
                
                # Manter apenas o perfil mais recente
                latest_profile = profiles.latest('id')
                logger.info(f"Mantendo perfil ID: {latest_profile.id} para {user.username} (Cliente: {latest_profile.cliente.nome})")
                
                # Excluir outros perfis
                for profile in profiles:
                    if profile.id != latest_profile.id:
                        logger.info(f"Excluindo perfil ID: {profile.id} para {user.username} (Cliente: {profile.cliente.nome})")
                        profile.delete()
            
            # Perguntar qual cliente usar para usuários sem perfil
            if users_without_profile:
                clientes = Cliente.objects.all()
                logger.info("Clientes disponíveis:")
                for i, cliente in enumerate(clientes):
                    logger.info(f"  {i+1}. {cliente.nome} (ID: {cliente.id})")
                
                logger.info("Digite o número do cliente para associar aos usuários sem perfil:")
                # Como estamos em um script, vamos usar o primeiro cliente
                cliente_index = 1
                
                try:
                    cliente = clientes[cliente_index - 1]
                    logger.info(f"Usando cliente: {cliente.nome} (ID: {cliente.id})")
                    
                    # Criar perfis para usuários sem perfil
                    for user in users_without_profile:
                        logger.info(f"Criando perfil para {user.username} com cliente {cliente.nome}")
                        Profile.objects.create(user=user, cliente=cliente)
                except (IndexError, ValueError):
                    logger.error("Índice de cliente inválido.")
        else:
            logger.info("Operação cancelada.")
    else:
        logger.info("Nenhum problema encontrado.")
    
    logger.info("Correção de perfis concluída.")

if __name__ == "__main__":
    fix_user_profiles()
