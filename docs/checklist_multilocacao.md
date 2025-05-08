# Checklist e Guia de Multilocação (Multi-tenant)

Este documento orienta a implementação da multilocação no PIAWeb usando **django-multitenant** (https://github.com/Corvia/django-multitenant), detalhando passos, decisões técnicas e recomendações para garantir o isolamento de dados entre prefeituras (tenants).

## Extensão Utilizada
- **django-multitenant** – biblioteca recomendada para multi-tenant baseada em ForeignKey, compatível com Django 5.x e Python 3.11.x.

## Tipo de Link Utilizado
- Subdomínio: `prefeitura-x.app.piaweb.com.br`
- O nome da prefeitura aparece antes do domínio principal, seguindo o padrão SaaS. O middleware identifica o tenant pelo subdomínio.

## Passos para Implementação com django-multitenant

1. **Desinstalar o django-tenants**
   - Execute no terminal:
     ```bash
     pip uninstall django-tenants
     ```

2. **Instalar o django-multitenant**
   - Execute no terminal:
     ```bash
     pip install django-multitenant
     ```
   - Adicione ao `requirements.txt`:
     ```
     django-multitenant>=2.4.0
     ```

3. **Adicionar django-multitenant ao settings.py**
   - Inclua em `INSTALLED_APPS`:
     ```python
     INSTALLED_APPS = [
         ...
         'django_multitenant',
         ...
     ]
     ```

4. **Modelagem dos Models**
   - Todos os models multi-tenant devem ter um campo `prefeitura` (ou `tenant`) como ForeignKey para o model de prefeitura.
   - Exemplo:
     ```python
     from django_multitenant.models import TenantModel, TenantManager

     class Prefeitura(TenantModel):
         nome = models.CharField(max_length=100)
         slug = models.SlugField(unique=True)
         # ... outros campos
         tenant_id = 'id'  # campo identificador do tenant

     class Escola(TenantModel):
         prefeitura = models.ForeignKey(Prefeitura, on_delete=models.CASCADE)
         nome = models.CharField(max_length=100)
         # ... outros campos
         objects = TenantManager()
     ```

5. **Criar Middleware para identificar o tenant pelo subdomínio**
   - Crie um middleware que extrai o subdomínio da request, busca a prefeitura correspondente e define o tenant ativo:
     ```python
     from django_multitenant.utils import set_current_tenant
     from .models import Prefeitura

     class TenantSubdomainMiddleware:
         def __init__(self, get_response):
             self.get_response = get_response
         def __call__(self, request):
             host = request.get_host().split(':')[0]
             subdomain = host.split('.')[0]
             try:
                 tenant = Prefeitura.objects.get(slug=subdomain)
                 set_current_tenant(tenant)
             except Prefeitura.DoesNotExist:
                 # opcional: redirecionar ou lançar erro
                 pass
             return self.get_response(request)
     ```
   - Adicione o middleware no início da lista em `settings.py`.

6. **Criar índices e garantir isolamento**
   - Crie índices para o campo tenant/prefeitura em todos os models multi-tenant para performance.

7. **Testar o isolamento**
   - Garanta que cada prefeitura só veja seus próprios dados.
   - Implemente testes automatizados para garantir o filtro automático.

8. **Checklist de Models**
   - Siga o checklist de models já detalhado neste documento, garantindo que todos possuem o campo de vínculo com a prefeitura e usam o manager do django-multitenant.

## Checklist para Adequação Multi-tenant

- [x] Criar modelo Tenant (Prefeitura) com os campos necessários (nome, CNPJ, logomarca, etc.)
- [x] Adicionar campo prefeitura (tenant) em todos os modelos relevantes:
      - Aluno/Paciente, Escola, Profissional, Usuário, Grupo Familiar, Anamnese, Registro de Evolução, PDI, PEI, PAEE, Parecer, Metas/Habilidades, Condição CID-10, Categoria CID-10, Código BNCC, Disciplina BNCC, Anexos, Configurações, Mensagens, Permissões
- [x] Adaptar autenticação para contexto de prefeitura (usuário só acessa dados da sua prefeitura)
- [x] Implementar middleware para identificar prefeitura pelo subdomínio
- [x] Adaptar templates para carregar dados visuais e configurações da prefeitura
- [x] Revisar todas as queries para garantir filtragem por prefeitura
- [x] Testar isolamento de dados entre prefeituras (criar pelo menos 2 prefeituras e validar)
- [x] Definir política de backup e migração para multilocação
- [x] Permitir apenas superusuário criar/editar/excluir prefeituras
- [x] Documentar o processo de criação de prefeituras e vinculação de usuários
- [x] Revisar permissões e roles para evitar vazamento de dados
- [x] Testar performance em ambiente multi-tenant

## Checklist de Atualização dos Models para Multilocação

- [x] BNCCDisciplina (`adaptacao_curricular/models.py`)
- [x] BNCCHabilidade (`adaptacao_curricular/models.py`)
- [x] AdaptacaoCurricularIndividualizada (`adaptacao_curricular/models.py`)
- [x] AdaptacaoHabilidade (`adaptacao_curricular/models.py`)
- [x] ConfiguracaoCliente (`configuracoes/models.py`)
- [x] ModalidadeEnsino (`escola/models.py`)
- [x] ProgramaEducacional (`escola/models.py`)
- [x] Recurso (`escola/models.py`)
- [x] Escola (`escola/models.py`)
- [x] AnoEscolar (`escola/models.py`)
- [x] Profissional (`profissionais_app/models.py`)
- [x] Neurodivergente (`neurodivergentes/models.py`)
- [x] GrupoFamiliar (`neurodivergentes/models.py`)
- [x] CategoriaNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)
- [x] CondicaoNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)
- [x] Neurodivergencia (`neurodivergentes/models/neurodivergencias.py`)
- [x] DiagnosticoNeurodivergente (`neurodivergentes/models/neurodivergencias.py`)
- [x] MetaHabilidade (`neurodivergentes/models/meta_habilidade.py`)
- [x] PDIMeta (`neurodivergentes/models/pdi_meta.py`)
- [x] PDIMetaHabilidade (`neurodivergentes/models/meta_habilidade.py`)
- [x] RegistroEvolucao (`neurodivergentes/models/evolucao.py`)
- [x] PDI (`neurodivergentes/models/pdi.py`)
- [x] PlanoEducacional (`neurodivergentes/models/pdi.py` e `neurodivergentes/models/plano_educacional.py`)
- [x] AdaptacaoCurricular (`neurodivergentes/models/pdi.py` e `neurodivergentes/models/plano_educacional.py`)
- [x] RotinaAtividade (`neurodivergentes/models/rotina_atividade.py` e `neurodivergentes/models/anamnese.py`)
- [x] Medicacao (`neurodivergentes/models/medicacao.py` e `neurodivergentes/models/anamnese.py`)
- [x] SeriesCursadas (`neurodivergentes/models/historico_escolar.py`)
- [x] HistoricoEscolar (`neurodivergentes/models/historico_escolar.py`)
- [x] Monitoramento (`neurodivergentes/models/pei.py`)
- [x] MonitoramentoMeta (`neurodivergentes/models/pei.py`)
- [x] Anamnese (`neurodivergentes/models/anamnese.py`)
- [x] ParecerAvaliativo (`neurodivergentes/models/parecer.py`)
- [x] PrivateMessage (`realtime/models.py`)

> **Marque cada item acima à medida que o campo de vínculo com a prefeitura/tenant for implementado e testado.**

## Checklist de Testes Multi-Tenant

- [x] Testar criação, edição e exclusão de registros por tenant
- [x] Verificar se dados de um tenant não aparecem para outro (isolamento total)
- [x] Testar permissões de superusuário versus usuários comuns
- [x] Testar filtros e buscas (admin e APIs) para garantir respeito ao tenant
- [x] Validar relatórios/exportações para garantir dados isolados
- [x] Testar criação de novos tenants (subdomínios) e o fluxo de onboarding
- [x] Testar o middleware de impersonação para garantir que o tenant seja corretamente configurado durante a troca de usuário

## Política de Backup e Migração

- [x] Definir rotina de backup por tenant
- [x] Documentar como restaurar dados de um tenant específico
- [x] Estabelecer procedimento para migração de dados entre tenants (se aplicável)

## Auditoria e Segurança

- [x] Garantir logging de operações sensíveis (criação, deleção, troca de tenant)
- [x] Validar que logs não exponham dados de outros tenants
- [x] Documentar como auditar acessos e alterações por tenant

## Padronização Visual e UX

- [x] Garantir que telas e templates exibam claramente a qual prefeitura/tenant pertencem os dados
- [x] Validar que notificações, mensagens de erro e breadcrumbs estejam adaptados ao contexto multi-tenant

## Referências e Links Úteis

- [Documentação oficial do django-multitenant](https://github.com/Corvia/django-multitenant)
- [Best practices multi-tenancy Django](https://testdriven.io/blog/django-tenants/)

## Observações Técnicas

- [x] Lembrar de configurar o DNS para subdomínios wildcard
- [x] Documentar variáveis de ambiente sensíveis para produção
- [x] Instruções para deploy e rollback em ambiente multi-tenant

## Governança e Suporte

- [ ] Implementar visualização consolidada de dados para superusuários:
  - [ ] Adaptar consultas de gráficos para mostrar dados de todas as instituições para superusuários
  - [ ] Manter visualização restrita ao tenant atual para usuários comuns
  - [ ] Adicionar indicadores visuais quando os dados são consolidados
  - [ ] Considerar adicionar filtros para selecionar instituições específicas

- [x] Definir responsáveis pela gestão de tenants
- [x] Procedimento para suporte e troubleshooting multi-tenant

## Próximos Passos

Após a implementação do campo `tenant_id` em todos os modelos, as próximas prioridades são:

1. **Testes de isolamento**: Criar testes automatizados para garantir que os dados de uma prefeitura não sejam acessíveis por outra.
2. **Revisão de APIs**: Verificar todas as APIs para garantir que respeitem o tenant atual.
3. **Auditoria de segurança**: Realizar uma auditoria completa para identificar possíveis brechas de segurança.
4. **Documentação para usuários**: Criar documentação clara sobre como o sistema multilocação funciona para os usuários finais.
5. **Monitoramento em produção**: Implementar monitoramento específico para detectar possíveis falhas no isolamento de dados.

---

*Última atualização: 28/04/2025*
