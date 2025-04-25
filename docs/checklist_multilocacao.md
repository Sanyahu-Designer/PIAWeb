# Checklist Técnico para Multilocação (Multi-tenant)

Este documento orienta os passos técnicos necessários para transformar a aplicação PIA em um sistema multilocatário, permitindo o atendimento de múltiplas prefeituras com isolamento seguro de dados e personalização visual.

---

## 1. Planejamento Inicial

- [x] Definir modelo de multilocação: **banco compartilhado** (campo prefeitura/tenant em todos os modelos).
- [x] Escolher pacote de multilocação: **django-tenants** (https://django-tenants.readthedocs.io/).
- [x] Mapear todos os modelos e funcionalidades que precisarão de isolamento por prefeitura (ver item abaixo).

### Modelos e funcionalidades que precisam de isolamento por prefeitura:

Todos os modelos que armazenam dados sensíveis ou operacionais devem ser vinculados a uma prefeitura (tenant). Com base na análise dos arquivos de modelos do projeto, seguem os principais:

- **Usuários** (`User`): cada usuário deve pertencer a uma prefeitura.
- **Profissionais** (`Profissional`)
- **Alunos/Pacientes** (`Neurodivergente`)
- **Grupo Familiar** (`GrupoFamiliar`)
- **Escolas** (`Escola`)
- **Ano Escolar** (`AnoEscolar`)
- **Modalidade de Ensino** (`ModalidadeEnsino`)
- **Programas Educacionais** (`ProgramaEducacional`)
- **Recursos** (`Recurso`)
- **Metas/Habilidades** (`BNCCHabilidade`, `BNCCDisciplina`)
- **Adaptação Curricular** (`AdaptacaoCurricularIndividualizada`, `AdaptacaoHabilidade`)
- **Configuração do Cliente** (`ConfiguracaoCliente`)
- **Mensagens/RealtTime** (`PrivateMessage`)
- **Outros modelos customizados** relacionados a relatórios, permissões, logs, uploads, anexos, etc.

**Funcionalidades que precisam de isolamento:**
- Cadastro, edição e visualização de todos os itens acima
- Relatórios e dashboards
- Uploads e anexos de arquivos
- Mensageria interna
- Permissões e grupos de usuários
- Personalização visual (logo, nome, cores, etc)
- Autenticação (login por subdomínio)
- Busca, filtros e exportações

**Observação:**
- Todos os relacionamentos entre modelos devem ser filtrados pela prefeitura/tenant.
- O superusuário global pode acessar todos os tenants, mas usuários comuns só veem dados da sua prefeitura.
- O middleware do django-tenants fará o isolamento automático, mas é fundamental garantir que todos os modelos estejam corretamente vinculados ao tenant.

---

## Tabela de Modelos Django no Projeto

Abaixo está uma tabela organizada com todos os modelos (`models.Model`) encontrados no projeto, incluindo seus respectivos arquivos. Use esta referência para revisão e documentação durante a implementação da arquitetura multi-tenant.

| Arquivo                                                         | Nome do Modelo                     |
|-----------------------------------------------------------------|------------------------------------|
| escola/models.py                                                | ModalidadeEnsino                   |
| escola/models.py                                                | ProgramaEducacional                |
| escola/models.py                                                | Recurso                            |
| escola/models.py                                                | Escola                             |
| escola/models.py                                                | AnoEscolar                         |
| profissionais_app/models.py                                     | Profissional                       |
| neurodivergentes/models/neurodivergencias.py                    | CategoriaNeurodivergente           |
| neurodivergentes/models/neurodivergencias.py                    | CondicaoNeurodivergente            |
| neurodivergentes/models/neurodivergencias.py                    | Neurodivergencia                   |
| neurodivergentes/models/neurodivergencias.py                    | DiagnosticoNeurodivergente         |
| neurodivergentes/models/pdi_meta.py                             | PDIMeta                            |
| neurodivergentes/models/meta_habilidade.py                      | MetaHabilidade                     |
| neurodivergentes/models/meta_habilidade.py                      | PDIMetaHabilidade                  |
| neurodivergentes/models/base.py                                 | Neurodivergente                    |
| neurodivergentes/models/pdi.py                                  | PDI                                |
| neurodivergentes/models/pdi.py                                  | PlanoEducacional                   |
| neurodivergentes/models/pdi.py                                  | AdaptacaoCurricular                |
| neurodivergentes/models/evolucao.py                             | RegistroEvolucao                   |
| neurodivergentes/models/grupo_familiar.py                       | GrupoFamiliar                      |
| neurodivergentes/models/rotina_atividade.py                     | RotinaAtividade                    |
| neurodivergentes/models/medicacao.py                            | Medicacao                          |
| neurodivergentes/models/historico_escolar.py                    | SeriesCursadas                     |
| neurodivergentes/models/historico_escolar.py                    | HistoricoEscolar                   |
| neurodivergentes/models/pei.py                                  | Monitoramento                      |
| neurodivergentes/models/pei.py                                  | MonitoramentoMeta                  |
| neurodivergentes/models/anamnese.py                             | Medicacao                          |
| neurodivergentes/models/anamnese.py                             | RotinaAtividade                    |
| neurodivergentes/models/anamnese.py                             | Anamnese                           |
| neurodivergentes/models/plano_educacional.py                    | PlanoEducacional                   |
| neurodivergentes/models/plano_educacional.py                    | AdaptacaoCurricular                |
| neurodivergentes/models/parecer.py                              | ParecerAvaliativo                  |
| neurodivergentes/models.py                                      | Neurodivergente                    |
| neurodivergentes/models.py                                      | GrupoFamiliar                      |
| realtime/models.py                                              | PrivateMessage                     |
| configuracoes/models.py                                         | ConfiguracaoCliente                |
| adaptacao_curricular/models.py                                  | BNCCDisciplina                     |
| adaptacao_curricular/models.py                                  | BNCCHabilidade                     |
| adaptacao_curricular/models.py                                  | AdaptacaoCurricularIndividualizada |
| adaptacao_curricular/models.py                                  | AdaptacaoHabilidade                |

> **Observação:** Alguns modelos possuem nomes repetidos em arquivos diferentes. Recomenda-se revisar se são entidades distintas ou se há duplicidade não intencional.

---

## Possibilidade de Migração para PostgreSQL

- [ ] Avaliar a migração do banco de dados de MariaDB para PostgreSQL para viabilizar o uso de soluções de multilocação mais robustas (ex: django-tenants)
- [ ] Planejar e testar a migração em ambiente de homologação
- [ ] Ajustar configurações do Django e dependências para PostgreSQL
- [ ] Documentar os passos e validar a integridade dos dados após a migração

> **Observação:** A migração para PostgreSQL abre caminho para isolamento por schema, maior segurança e escalabilidade, sendo a opção mais recomendada para multilocação avançada.

## Roteiro Detalhado de Migração: MariaDB → PostgreSQL

### 1. Planejamento e Preparação
- [ ] Fazer backup completo do banco MariaDB e do código-fonte
- [ ] Listar todas as tabelas, relacionamentos e tipos de dados especiais
- [ ] Revisar dependências e bibliotecas do projeto para garantir compatibilidade com PostgreSQL

### 2. Configuração do PostgreSQL
- [ ] Instalar o PostgreSQL no ambiente de desenvolvimento/homologação
- [ ] Criar um novo banco de dados e usuário para o projeto
- [ ] Ajustar o arquivo `settings.py` do Django para usar o backend `django.db.backends.postgresql`

### 3. Ferramentas de Migração
- [ ] Considerar uso de ferramentas como:
    - [`pgloader`](https://pgloader.io/) (automatiza a migração de dados e converte tipos)
    - [`Django Database Migration Tool`](https://github.com/urbanze/django-db-migrate)
    - Exportação para CSV + importação manual (para bases menores)

### 4. Migração dos Dados
- [ ] Exportar os dados do MariaDB (dump SQL ou CSV)
- [ ] Importar os dados no PostgreSQL utilizando a ferramenta escolhida
- [ ] Ajustar tipos de dados incompatíveis (ex: `TINYINT` → `BOOLEAN`, `DATETIME` → `TIMESTAMP`)

### 5. Recriação das Migrações Django
- [ ] Apagar as migrações antigas (`migrations/`), se necessário (cuidado: só faça isso se for migrar tudo do zero)
- [ ] Rodar `python manage.py makemigrations` e `python manage.py migrate` no novo banco PostgreSQL
- [ ] Validar se todas as tabelas e constraints foram criadas corretamente

### 6. Testes de Integridade
- [ ] Comparar amostras de dados entre os bancos antigo e novo
- [ ] Testar todas as funcionalidades críticas do sistema
- [ ] Executar testes automatizados e revisar logs de erro

### 7. Ajustes Finais
- [ ] Atualizar configurações de produção (ambiente, backups, monitoramento)
- [ ] Documentar todo o processo e eventuais ajustes feitos
- [ ] Treinar a equipe para uso e manutenção do PostgreSQL

### 8. Go Live
- [ ] Planejar um período de manutenção para a migração final (downtime, se necessário)
- [ ] Fazer backup final do MariaDB antes do corte
- [ ] Executar a migração definitiva e ativar o sistema em PostgreSQL

> **Dicas:**
> - Faça a migração primeiro em ambiente de homologação, nunca direto na produção.
> - Ferramentas como o `pgloader` facilitam a conversão automática de tipos e estrutura.
> - Teste queries e relatórios após a migração, pois sintaxes podem mudar entre MariaDB e PostgreSQL.
> - Se possível, mantenha o MariaDB em modo somente leitura por um período após o go live, como contingência.

---

## Opções de Multilocação por Banco de Dados

### 1. Utilizando PostgreSQL
- **django-tenants** (https://django-tenants.readthedocs.io/)
    - Isolamento por schema (cada tenant em um schema separado)
    - Segurança e isolamento fortes
    - Recomendado para projetos que podem utilizar PostgreSQL

### 2. Utilizando MariaDB/MySQL
- **django-multitenant** (https://github.com/Corvia/django-multitenant)
    - Compatível com MariaDB/MySQL
    - Isolamento lógico por campo identificador de tenant (ex: `prefeitura_id`)
    - Requer atenção para garantir que todas as queries sejam filtradas pelo tenant
    - Pode ser implementado também manualmente, com managers e middlewares customizados

> **Observação:** Avalie a possibilidade de migração para PostgreSQL caso deseje isolamento mais forte via schemas. Para MariaDB, a abordagem via campo identificador de tenant é a mais comum e segura.

---

## Checklist de Segurança e Preparação para Multilocação

Antes de iniciar a implementação, siga este checklist para garantir um processo seguro e controlado:

- [ ] **Backup Completo**
    - [ ] Realizar backup atualizado do banco de dados
    - [ ] Realizar backup do código-fonte

- [ ] **Revisão dos Modelos**
    - [ ] Conferir se todos os modelos segregáveis estão mapeados
    - [ ] Revisar possíveis duplicidades de nomes de modelos

- [ ] **Dependências e Versões**
    - [ ] Verificar se o pacote `django-tenants` está instalado e compatível
    - [ ] Confirmar que as dependências do projeto estão atualizadas

- [ ] **Mapeamento de Funcionalidades**
    - [ ] Listar funcionalidades críticas que exigem isolamento por prefeitura
    - [ ] Identificar pontos de risco para vazamento de dados entre tenants

- [ ] **Configuração do Ambiente**
    - [ ] Garantir ambientes separados para desenvolvimento, homologação e produção
    - [ ] Preparar scripts de migração e testes automatizados

- [ ] **Estratégia de Migração**
    - [ ] Planejar adição do campo `prefeitura` nos modelos existentes
    - [ ] Definir valores padrão e estratégia para migração de dados antigos
    - [ ] Avaliar necessidade de downtime

- [ ] **Documentação e Comunicação**
    - [ ] Documentar todas as mudanças planejadas
    - [ ] Comunicar equipe sobre impactos e etapas

- [ ] **Testes**
    - [ ] Elaborar plano de testes para validar funcionalidades após multilocação
    - [ ] Incluir testes para garantir isolamento entre tenants

---

## 2. Modelos de Dados

- [ ] Criar modelo `Prefeitura` (ou `Tenant`) com campos: nome, domínio, logo, etc.
- [ ] Adicionar campo `prefeitura` (ForeignKey) em todos os modelos que armazenam dados segregáveis (Alunos, Escolas, Profissionais, Usuários, etc).
- [ ] Atualizar relacionamentos entre modelos para garantir integridade referencial.
- [ ] Criar e aplicar migrações no banco de dados.

---

## 3. Middleware e Identificação do Tenant

- [ ] Implementar middleware para identificar a prefeitura pelo subdomínio ou domínio customizado.
- [ ] Garantir que o contexto da prefeitura esteja disponível em todos os requests (request.prefeitura ou similar).
- [ ] Adaptar rotas e URLs para funcionar corretamente no contexto do tenant.

---

## 4. Autenticação e Usuários

- [ ] Adaptar fluxo de login para funcionar por subdomínio/domínio.
- [ ] Garantir que cada usuário esteja vinculado a uma prefeitura.
- [ ] Revisar permissões, grupos e autenticação para garantir acesso apenas aos dados do tenant correto.
- [ ] Adaptar criação de usuários para já associar à prefeitura correta.

---

## 5. Queries, Views e APIs

- [ ] Revisar todas as queries para garantir filtragem por prefeitura.
- [ ] Adaptar views, managers e forms para operar no contexto do tenant.
- [ ] Adaptar APIs (Django REST Framework, etc) para garantir isolamento dos dados.
- [ ] Revisar relatórios, exportações e dashboards para garantir que só mostrem dados do tenant atual.

---

## 6. Templates e Personalização Visual

- [ ] Adaptar templates para carregar logo, nome e cores da prefeitura.
- [ ] Garantir que todos os templates usem o contexto do tenant.
- [ ] Adaptar breadcrumbs, cabeçalhos e rodapés para exibir informações da prefeitura.

---

## 7. Migração de Dados

- [ ] Planejar estratégia de migração dos dados existentes (se já houver dados de múltiplas prefeituras).
- [ ] Escrever scripts de migração para associar registros à prefeitura correta.
- [ ] Validar integridade dos dados pós-migração.

---

## 8. Testes

- [ ] Criar testes automatizados para garantir isolamento de dados entre prefeituras.
- [ ] Testar autenticação, permissões, relatórios, uploads e visualização de dados.
- [ ] Testar criação, edição e exclusão de registros em diferentes prefeituras.
- [ ] Testar personalização visual por prefeitura.

---

## 9. Documentação e Suporte

- [ ] Documentar arquitetura de multilocação adotada.
- [ ] Documentar como cadastrar novas prefeituras e usuários.
- [ ] Documentar procedimentos de backup, restore e migração.
- [ ] Treinar equipe de suporte e desenvolvimento para o novo fluxo.

---

## 10. Pós-implementação

- [ ] Monitorar logs para identificar possíveis vazamentos de dados entre prefeituras.
- [ ] Coletar feedback dos usuários administradores de cada prefeitura.
- [ ] Planejar melhorias contínuas e possíveis ajustes de performance.

---

## Recomendações Avançadas para Multilocação

- [ ] **Monitoramento e Logs**
    - [ ] Configurar logs de acesso e erros por tenant para facilitar auditoria e troubleshooting
    - [ ] Garantir que logs sensíveis não exponham dados de outros tenants

- [ ] **Permissões e Autenticação**
    - [ ] Revisar regras de permissão para garantir que usuários só acessem dados do próprio tenant
    - [ ] Adaptar middlewares/autenticação para o contexto multi-tenant

- [ ] **Interface e Experiência do Usuário**
    - [ ] Personalizar visualmente o sistema conforme o tenant (logo, cores, textos institucionais)
    - [ ] Garantir que todos os textos e labels estejam padronizados conforme as memórias de design (ex: “Adicionar”, “Salvar”, etc)

- [ ] **Performance e Escalabilidade**
    - [ ] Avaliar consultas e índices para evitar lentidão em cenários multi-tenant
    - [ ] Testar performance com múltiplos tenants e volume de dados

- [ ] **Política de Backup e Recuperação**
    - [ ] Definir e documentar políticas de backup e restore por tenant, se necessário

- [ ] **Treinamento e Suporte**
    - [ ] Preparar material de treinamento para equipe de suporte/administração sobre o funcionamento do multi-tenant
    - [ ] Documentar procedimentos de onboarding de novos tenants

- [ ] **Compliance e LGPD**
    - [ ] Revisar o sistema quanto a requisitos de privacidade e proteção de dados (LGPD/GDPR), garantindo isolamento total entre tenants

Este checklist deve ser revisado e atualizado conforme o andamento do projeto e as necessidades específicas da aplicação.
