# Análise de Models para Isolamento de Dados (LGPD)

> **NOTA DE ATUALIZAÇÃO (28/04/2025)**: Todas as recomendações deste documento foram implementadas. O campo `tenant_id` foi adicionado a todos os modelos que herdam de `TenantModel`, garantindo o isolamento adequado de dados entre as prefeituras conforme exigido pela LGPD.

Este documento apresenta uma análise detalhada de todos os models listados no checklist_multilocacao.md, verificando se estão corretamente configurados para garantir o isolamento de dados entre tenants (prefeituras) e conformidade com a LGPD.

## Metodologia de Análise

Para cada model, verificamos:

1. **Herança de TenantModel**: O model deve herdar de `TenantModel` para garantir o isolamento de dados.
2. **Campo de Tenant**: Deve existir um campo `cliente` ou equivalente como ForeignKey para o model `Cliente`.
3. **TenantManager**: O model deve usar `TenantManager` para consultas.
4. **Uso nas Views**: Como o model é usado nas views, especialmente durante a impersonação.

## Análise dos Models

### 1. Cliente (`clientes/models.py`)

```python
class Cliente(TenantModel):
    nome = models.CharField(max_length=200, verbose_name="Nome da Prefeitura ou Cliente")
    cnpj = models.CharField(max_length=18, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    tenant_id = 'id'  # Campo usado pelo django-multitenant para isolar os dados

    def __str__(self):
        return self.nome
```

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Define `tenant_id = 'id'` corretamente
- ⚠️ Não usa `TenantManager`, mas como é o model principal de tenant, isso é aceitável
- 🔴 Risco: Como model principal de tenant, deve ser protegido contra exclusão acidental

### 2. Neurodivergente (`neurodivergentes/models.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados pessoais sensíveis que devem ser isolados por tenant

### 3. Escola (`escola/models.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🟡 Risco Médio: Contém dados institucionais que devem ser isolados por tenant

### 4. Profissional (`profissionais_app/models.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados pessoais de profissionais que devem ser isolados por tenant

### 5. PDI (`neurodivergentes/models/pdi.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados sensíveis sobre o plano de desenvolvimento individual de alunos

### 6. Anamnese (`neurodivergentes/models/anamnese.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco Alto: Contém dados médicos e históricos sensíveis que exigem proteção rigorosa

### 7. RegistroEvolucao (`neurodivergentes/models/evolucao.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados de evolução do aluno que devem ser isolados por tenant

### 8. GrupoFamiliar (`neurodivergentes/models.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados familiares sensíveis que devem ser isolados por tenant

### 9. CategoriaNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🟡 Risco Médio: Contém categorias de neurodivergência que devem ser isoladas por tenant

### 10. CondicaoNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🟡 Risco Médio: Contém condições de neurodivergência que devem ser isoladas por tenant

### 11. Neurodivergencia (`neurodivergentes/models/neurodivergencias.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém dados sensíveis sobre neurodivergências específicas de alunos

### 12. DiagnosticoNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco Alto: Contém diagnósticos médicos sensíveis que exigem proteção rigorosa

### 13. MetaHabilidade (`neurodivergentes/models/meta_habilidade.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🟡 Risco Médio: Contém metas e habilidades que devem ser isoladas por tenant

### 14. PDIMeta (`neurodivergentes/models/pdi_meta.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém metas específicas de PDIs que devem ser isoladas por tenant

### 15. PDIMetaHabilidade (`neurodivergentes/models/meta_habilidade.py`)

**Análise**:
- ✅ Herda de `TenantModel`
- ✅ Possui campo `cliente` como ForeignKey para `Cliente`
- ✅ Usa `TenantManager`
- 🔴 Risco: Contém habilidades específicas de PDIs que devem ser isoladas por tenant

## Problemas Identificados nas Views

Após analisar os models, identificamos os seguintes problemas nas views que podem levar a vazamentos de dados:

### 1. Dashboard Principal (`pia_config/views.py`)

```python
@login_required
def dashboard(request):
    # Consultas que podem não estar respeitando o tenant durante a impersonação
    alunos_query = Neurodivergente.objects.all()
    # ...
```

**Risco**: As consultas podem não estar respeitando o tenant atual durante a impersonação.

### 2. APIs de Dados (`neurodivergentes/api_views.py`)

```python
@login_required
def api_genero_por_neurodivergencia(request):
    # Consultas que podem não estar respeitando o tenant durante a impersonação
    dados = Neurodivergencia.objects.values('genero').annotate(total=Count('id'))
    # ...
```

**Risco**: As APIs podem estar retornando dados de todos os tenants durante a impersonação.

### 3. Listagem de Usuários (`usuarios/views.py`)

```python
@login_required
def usuarios_da_minha_prefeitura(request):
    # Já corrigido para respeitar o tenant durante a impersonação
    # ...
```

**Risco**: Corrigido, mas pode haver outras views similares não corrigidas.

## Recomendações para Correção

1. **Implementar o Middleware de Tenant Global** conforme descrito no documento `correcao_seguranca_tenant.md`.

2. **Revisar Todas as Views** que fazem consultas ao banco de dados para garantir que estejam usando o `TenantManager` corretamente.

3. **Adicionar Validações de Segurança** em todas as views que manipulam dados sensíveis:

```python
def view_sensivel(request, objeto_id):
    # Verificar se o objeto pertence ao tenant atual
    objeto = get_object_or_404(ModeloSensivel, id=objeto_id)
    
    # Se for superusuário em modo de impersonação, verificar se o objeto pertence ao tenant impersonado
    if request.user.is_superuser and hasattr(request, 'is_impersonating') and request.is_impersonating:
        if objeto.cliente.id != request.impersonated_cliente.id:
            return HttpResponseForbidden("Acesso negado: este objeto não pertence à prefeitura impersonada.")
    
    # Se for usuário normal, verificar se o objeto pertence ao seu tenant
    elif not request.user.is_superuser:
        profile = getattr(request.user, 'profile', None)
        if not profile or objeto.cliente.id != profile.cliente.id:
            return HttpResponseForbidden("Acesso negado: este objeto não pertence à sua prefeitura.")
    
    # Continuar com a view normalmente
    # ...
```

4. **Implementar Logs de Auditoria** para registrar acessos a dados sensíveis:

```python
import logging
audit_logger = logging.getLogger('audit')

def view_sensivel(request, objeto_id):
    # ...
    
    # Registrar acesso aos dados
    audit_logger.info(
        f"Acesso a dados sensíveis: user={request.user.username}, "
        f"tenant={objeto.cliente.nome}, objeto_id={objeto_id}, "
        f"impersonating={getattr(request, 'is_impersonating', False)}"
    )
    
    # ...
```

5. **Implementar Testes Automatizados** para verificar o isolamento de dados entre tenants.

## Conclusão

A análise dos models mostra que eles estão corretamente configurados para o isolamento de dados entre tenants, mas há riscos significativos nas views que podem não estar respeitando esse isolamento durante a impersonação.

A implementação das recomendações deste documento e do documento `correcao_seguranca_tenant.md` é essencial para garantir a conformidade com a LGPD e evitar vazamentos de dados sensíveis entre diferentes prefeituras.
