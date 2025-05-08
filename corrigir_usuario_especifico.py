#!/usr/bin/env python
"""
Script para corrigir um usuário específico que não tem perfil.
Este script deve ser executado usando o shell do Django:
    python manage.py shell < corrigir_usuario_especifico.py
"""

import logging
from django.contrib.auth.models import User
from clientes.models_profile import Profile
from clientes.models import Cliente

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Nome do usuário a ser corrigido - ALTERE PARA O NOME DO SEU USUÁRIO
NOME_USUARIO = 'sap_user_2'  # Altere para o nome do usuário que você criou

# ID do cliente (prefeitura) ao qual o usuário deve ser associado
# Prefeitura Municipal de Santo Antonio da Patrulha = 4
CLIENTE_ID = 4  # Altere para o ID do cliente correto

try:
    # Buscar o usuário
    usuario = User.objects.get(username=NOME_USUARIO)
    logger.info(f"Usuário encontrado: {usuario.username} (ID: {usuario.id})")
    
    # Buscar o cliente
    cliente = Cliente.objects.get(id=CLIENTE_ID)
    logger.info(f"Cliente encontrado: {cliente.nome} (ID: {cliente.id})")
    
    # Verificar se o usuário já tem um perfil
    try:
        perfil = Profile.objects.get(user=usuario)
        logger.info(f"Perfil existente encontrado. Cliente atual: {perfil.cliente.nome} (ID: {perfil.cliente.id})")
        
        # Atualizar o cliente do perfil
        perfil.cliente = cliente
        perfil.save()
        logger.info(f"Perfil atualizado para o cliente: {cliente.nome} (ID: {cliente.id})")
    except Profile.DoesNotExist:
        # Criar um novo perfil
        perfil = Profile(user=usuario, cliente=cliente)
        perfil.save()
        logger.info(f"Novo perfil criado para o cliente: {cliente.nome} (ID: {cliente.id})")
    except Profile.MultipleObjectsReturned:
        # Excluir todos os perfis e criar um novo
        Profile.objects.filter(user=usuario).delete()
        logger.info("Múltiplos perfis encontrados e excluídos.")
        
        perfil = Profile(user=usuario, cliente=cliente)
        perfil.save()
        logger.info(f"Novo perfil criado para o cliente: {cliente.nome} (ID: {cliente.id})")
    
    logger.info("Correção concluída com sucesso!")
except User.DoesNotExist:
    logger.error(f"Usuário '{NOME_USUARIO}' não encontrado.")
except Cliente.DoesNotExist:
    logger.error(f"Cliente com ID {CLIENTE_ID} não encontrado.")
except Exception as e:
    logger.error(f"Erro: {str(e)}")
