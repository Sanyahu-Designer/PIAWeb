# Correção de Segurança para Isolamento de Dados (LGPD)

> **NOTA DE ATUALIZAÇÃO (28/04/2025)**: Todas as correções descritas neste documento foram implementadas. O campo `tenant_id` foi adicionado a todos os modelos que herdam de `TenantModel` e o middleware de tenant foi corrigido para configurar corretamente o tenant atual.

Este documento descreve os problemas identificados no sistema PIA relacionados ao isolamento de dados entre tenants (prefeituras) e propõe soluções para garantir a conformidade com a LGPD.

## Problemas Identificados

### 1. Falha na Configuração do Tenant Durante Impersonação

**Problema Crítico**: O middleware de impersonação (`ImpersonationMiddleware`) define `request.impersonated_cliente` e `request.is_impersonating`, mas **não configura o tenant atual** para o django_multitenant.

```python
# No middleware atual
request.is_impersonating = True
request.impersonated_cliente = cliente
# Falta: set_current_tenant(cliente)
```

Isso significa que o sistema pode estar usando o tenant errado nas consultas ao banco de dados, permitindo que um superusuário em modo de impersonação veja dados de todas as prefeituras, não apenas da prefeitura impersonada.

### 2. Inconsistência nas Consultas ao Banco de Dados

Muitas views foram modificadas para verificar se o usuário está no modo de impersonação, mas não há garantia de que todas as consultas ao banco de dados estejam sendo filtradas corretamente pelo tenant atual.

Por exemplo, nas views modificadas:
```python
if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
    cliente = request.impersonated_cliente
    # As consultas aqui usam cliente diretamente, mas podem não estar usando o tenant_id corretamente
```

### 3. APIs e Endpoints Não Verificados

Existem vários endpoints de API no sistema (como `/api/genero-por-neurodivergencia/`, `/api/distribuicao-por-neurodivergencia/`, etc.) que podem não estar respeitando o contexto de impersonação e podem estar retornando dados de todas as prefeituras.

### 4. Falta de Middleware de Tenant Global

O sistema usa `django_multitenant`, mas não há um middleware global que configure o tenant atual com base no usuário ou na sessão de impersonação. Isso pode levar a consultas inconsistentes.

### 5. Logs e Informações Sensíveis

O middleware atual imprime informações de debug no console:
```python
print(f"IMPERSONANDO CLIENTE: {cliente.id} - {cliente.nome}")
```

Isso pode expor informações sensíveis em logs de produção, o que é uma violação da LGPD.

### 6. Ausência de Testes de Isolamento

Não há evidências de testes automatizados que verifiquem se o isolamento de dados entre tenants está funcionando corretamente, especialmente durante a impersonação.

## Soluções Propostas

### 1. Corrigir o Middleware de Impersonação

Modificar o middleware de impersonação para configurar corretamente o tenant atual:

```python
# clientes/middleware.py
from django_multitenant.utils import set_current_tenant
from clientes.models import Cliente
import logging

logger = logging.getLogger(__name__)

class ImpersonationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se há uma sessão de impersonação ativa
        if request.user.is_authenticated and request.user.is_superuser:
            impersonated_cliente_id = request.session.get('impersonated_cliente_id')
            if impersonated_cliente_id:
                try:
                    cliente = Cliente.objects.get(id=impersonated_cliente_id)
                    # Log para debug (usando logger em vez de print)
                    logger.debug(f"Impersonando cliente: {cliente.id} - {cliente.nome}")
                    
                    request.is_impersonating = True
                    request.impersonated_cliente = cliente
                    
                    # Configurar o tenant atual para o django_multitenant
                    set_current_tenant(cliente)
                    
                except Cliente.DoesNotExist:
                    # Se o cliente não existir mais, limpa a sessão
                    request.is_impersonating = False
                    if 'impersonated_cliente_id' in request.session:
                        del request.session['impersonated_cliente_id']
                    if 'impersonated_cliente_name' in request.session:
                        del request.session['impersonated_cliente_name']
            else:
                request.is_impersonating = False
        else:
            request.is_impersonating = False

        response = self.get_response(request)
        return response
```

### 2. Implementar um Middleware Global de Tenant

Criar um novo middleware que configure o tenant atual com base no usuário autenticado:

```python
# clientes/middleware.py
from django_multitenant.utils import set_current_tenant
from clientes.models import Cliente
from clientes.models_profile import Profile
import logging

logger = logging.getLogger(__name__)

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Limpa qualquer tenant configurado anteriormente
        set_current_tenant(None)
        
        # Se o usuário está autenticado
        if request.user.is_authenticated:
            # Se é um superusuário em modo de impersonação
            if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
                cliente = request.impersonated_cliente
                set_current_tenant(cliente)
                logger.debug(f"Tenant configurado para impersonação: {cliente.id} - {cliente.nome}")
            # Se é um usuário normal (não superusuário)
            elif not request.user.is_superuser:
                try:
                    # Busca o profile do usuário para obter o cliente
                    profile = Profile.objects.get(user=request.user)
                    cliente = profile.cliente
                    set_current_tenant(cliente)
                    logger.debug(f"Tenant configurado para usuário: {cliente.id} - {cliente.nome}")
                except Profile.DoesNotExist:
                    logger.warning(f"Usuário {request.user.username} não tem profile associado")
        
        response = self.get_response(request)
        return response
```

### 3. Atualizar o settings.py para incluir o novo middleware

```python
# pia_config/settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'clientes.middleware.ImpersonationMiddleware',
    'clientes.middleware.TenantMiddleware',  # Adicionar este middleware após o ImpersonationMiddleware
]
```

### 4. Revisar as Views de API

Modificar todas as views de API para respeitar o tenant atual:

```python
# Exemplo para uma view de API
@login_required
def api_genero_por_neurodivergencia(request):
    # Se for superusuário no modo de impersonação, usa o tenant impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        # O tenant já deve estar configurado pelo middleware
        pass
    # Se for usuário normal, usa seu próprio tenant
    elif not request.user.is_superuser:
        # O tenant já deve estar configurado pelo middleware
        pass
    # Se for superusuário sem impersonação, retorna erro ou dados agregados
    else:
        return JsonResponse({"error": "Selecione uma prefeitura para visualizar os dados"})
    
    # Agora as consultas usando TenantManager já devem respeitar o tenant atual
    dados = Neurodivergencia.objects.values('genero').annotate(total=Count('id'))
    return JsonResponse(list(dados), safe=False)
```

### 5. Implementar Testes de Isolamento

Criar testes automatizados para verificar o isolamento de dados entre tenants:

```python
# clientes/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from clientes.models import Cliente
from clientes.models_profile import Profile
from neurodivergentes.models import Neurodivergente
from django_multitenant.utils import set_current_tenant

class TenantIsolationTest(TestCase):
    def setUp(self):
        # Criar dois clientes (prefeituras)
        self.cliente1 = Cliente.objects.create(nome="Prefeitura 1", cnpj="11.111.111/0001-11", slug="prefeitura-1")
        self.cliente2 = Cliente.objects.create(nome="Prefeitura 2", cnpj="22.222.222/0001-22", slug="prefeitura-2")
        
        # Criar um superusuário
        self.superuser = User.objects.create_superuser(username="admin", email="admin@example.com", password="admin123")
        
        # Criar usuários para cada prefeitura
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="user1123")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="user2123")
        
        # Criar profiles para cada usuário
        Profile.objects.create(user=self.user1, cliente=self.cliente1)
        Profile.objects.create(user=self.user2, cliente=self.cliente2)
        
        # Criar dados para cada prefeitura
        set_current_tenant(self.cliente1)
        self.aluno1 = Neurodivergente.objects.create(nome="Aluno 1", cliente=self.cliente1)
        
        set_current_tenant(self.cliente2)
        self.aluno2 = Neurodivergente.objects.create(nome="Aluno 2", cliente=self.cliente2)
        
        # Limpar o tenant atual
        set_current_tenant(None)
        
        # Cliente para testes HTTP
        self.client = Client()
    
    def test_usuario_ve_apenas_seus_dados(self):
        # Login como user1 (Prefeitura 1)
        self.client.login(username="user1", password="user1123")
        
        # Verificar se user1 vê apenas os dados da Prefeitura 1
        response = self.client.get('/dashboard/')
        self.assertContains(response, "Aluno 1")
        self.assertNotContains(response, "Aluno 2")
        
        # Login como user2 (Prefeitura 2)
        self.client.logout()
        self.client.login(username="user2", password="user2123")
        
        # Verificar se user2 vê apenas os dados da Prefeitura 2
        response = self.client.get('/dashboard/')
        self.assertContains(response, "Aluno 2")
        self.assertNotContains(response, "Aluno 1")
    
    def test_impersonacao_ve_apenas_dados_do_cliente_impersonado(self):
        # Login como superuser
        self.client.login(username="admin", password="admin123")
        
        # Impersonar Prefeitura 1
        self.client.get(f'/clientes/impersonate/{self.cliente1.id}/')
        
        # Verificar se vê apenas os dados da Prefeitura 1
        response = self.client.get('/dashboard/')
        self.assertContains(response, "Aluno 1")
        self.assertNotContains(response, "Aluno 2")
        
        # Parar impersonação
        self.client.get('/clientes/stop-impersonation/')
        
        # Impersonar Prefeitura 2
        self.client.get(f'/clientes/impersonate/{self.cliente2.id}/')
        
        # Verificar se vê apenas os dados da Prefeitura 2
        response = self.client.get('/dashboard/')
        self.assertContains(response, "Aluno 2")
        self.assertNotContains(response, "Aluno 1")
```

## Checklist de Verificação de Models

Para garantir que todos os models estejam configurados corretamente para o isolamento de dados, verifique se:

1. Todos os models que devem ser isolados por tenant herdam de `TenantModel`
2. Todos os models têm um campo `cliente` ou `tenant` como ForeignKey para o model `Cliente`
3. Todos os models usam o `TenantManager` para consultas
4. O campo `tenant_id` está definido corretamente no model `Cliente`

### Exemplo de Model Correto:

```python
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente

class Neurodivergente(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    # ... outros campos
    
    objects = TenantManager()
```

## Plano de Implementação

1. Implementar as correções no middleware de impersonação
2. Adicionar o novo middleware global de tenant
3. Revisar todas as views de API para garantir que respeitem o tenant atual
4. Implementar testes automatizados para verificar o isolamento de dados
5. Revisar todos os models listados no checklist_multilocacao.md
6. Realizar testes manuais para garantir que o isolamento de dados está funcionando corretamente
7. Documentar as mudanças e treinar a equipe sobre as melhores práticas de isolamento de dados

## Conformidade com a LGPD

Estas correções são essenciais para garantir a conformidade com a LGPD, especificamente:

- **Art. 6º, VII**: Garantia da segurança dos dados pessoais
- **Art. 46**: Adoção de medidas de segurança para proteção dos dados pessoais
- **Art. 47**: Responsabilidade por danos decorrentes de violação da segurança dos dados

A implementação correta do isolamento de dados entre tenants é fundamental para evitar vazamentos de dados e garantir a conformidade com a LGPD.
