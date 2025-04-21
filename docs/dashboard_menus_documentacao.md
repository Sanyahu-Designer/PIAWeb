# Documentação dos Menus do Dashboard

Esta documentação detalha o objetivo e as funcionalidades de cada módulo do menu sidebar e do menu do usuário do sistema, servindo de base para a implementação do tour guiado (Bootstrap Tour) e para padronização da experiência do usuário.

## 1. Menu Sidebar

### Módulos do Sistema (Menus de Aplicações)
- **Ícone:** variável, conforme configuração do app (ex: usuários, grupos, relatórios, etc.)
- **Objetivo:** Exibe uma lista de módulos e funcionalidades cadastradas no sistema, agrupadas por aplicação. Cada módulo pode conter subitens para acesso rápido a funcionalidades específicas (ex: cadastro de alunos, profissionais, relatórios).

#### Módulos detalhados:

- **Alunos/Pacientes**
 - **Ícone:** usuário (`fas fa-user` ou similar)
 - **Objetivo:** Permite acessar a listagem, cadastrar, editar e imprimir o relatório com os dados pessoais de cada Aluno/Paciente atendidos pelo sistema.
 - **Funcionalidades:** Busca avançada, filtros por status, acesso ao prontuário, impressão de documentos e geração de relatórios.

- **Anamneses**
 - **Ícone:** descrição (`fas fa-description` ou similar)
 - **Objetivo:** Permite gerenciar registros de anamnese dos alunos/pacientes, com histórico detalhado de informações clínicas, sociais e educacionais coletadas no início do acompanhamento.
 - **Funcionalidades:** Visualização por paciente, impressão, histórico de alterações e integração com o prontuário.

- **Histórico de Evolução**
 - **Ícone:** histórico (`fas fa-history` ou similar)
 - **Objetivo:** Permite registrar e acompanhar as evoluções clínicas, educacionais e comportamentais dos alunos/pacientes ao longo do tempo. Permite observações de diferentes profissionais, anexos e encaminhamentos.
 - **Funcionalidades:** Filtros por data/profissional, anexos e comentários.

- **Neurodivergentes**
 - **Ícone:** cérebro (`fas fa-brain` ou similar)
 - **Objetivo:** Permite cadastrar diagnósticos, visualizar e imprimir o perfil dos alunos/pacientes com neurodivergências. Permite acessar laudos e documentos importantes.
 - **Funcionalidades:** Cadastro completo, upload de documentos e profissionais responsáveis.

- **PAEE (Plano de Atendimento Educacional Especializado)**
 - **Ícone:** plano especializado (`fas fa-chalkboard-teacher` ou similar)
 - **Objetivo:** Permite gerenciar o Plano de Atendimento Educacional Especializado, registrando Metas/Habilidades e fazer o Planejamento sobre intervenções e apoios necessários para o Aluno/Paciente.
 - **Funcionalidades:** Cadastro, edição, acompanhamento de intervenções, anexos e relatórios.

- **PDI (Plano de Desenvolvimento Individual)**
 - **Ícone:** plano individual (`fas fa-file-contract` ou similar)
 - **Objetivo:** Permite gerenciar o Plano de Desenvolvimento Individual dos Alunos/Pacientes, definindo metas, estratégias, intervenções e acompanhamento do progresso do Aluno/Paciente ao longo do tempo.
 - **Funcionalidades:** Cadastro, edição, acompanhamento de metas e estratégias, anexos, impressão, histórico de revisões e integração com registros de evolução e relatórios.

- **PEI (Plano Educacional Individualizado)**
 - **Ícone:** documento personalizado (`fas fa-file-signature` ou similar)
 - **Objetivo:** Permite gerenciar o Plano Educacional Individualizado dos alunos/pacientes, detalhando estratégias pedagógicas, adaptações e metas específicas para o desenvolvimento educacional.
 - **Funcionalidades:** Cadastro, edição, acompanhamento de objetivos, anexos, impressão e histórico de revisões.

- **Pareceres**
 - **Ícone:** parecer (`fas fa-file-alt` ou similar)
 - **Objetivo:** Permite gerenciar pareceres técnicos, pedagógicos ou clínicos emitidos por profissionais da equipe multidisciplinar.
 - **Funcionalidades:** Cadastro, edição, anexos, histórico e impressão de pareceres.

- **Código BNCC**
 - **Ícone:** código de barras (`fas fa-barcode` ou similar)
 - **Objetivo:** Permite cadastrar e gerenciar os códigos da Base Nacional Comum Curricular (BNCC), permitindo o cadastro e consulta de componentes curriculares e habilidades padronizadas.
 - **Funcionalidades:** Cadastro, edição, busca, consulta rápida e vínculo com disciplinas e habilidades.

- **Disciplinas BNCC**
 - **Ícone:** disciplinas (`fas fa-book` ou similar)
 - **Objetivo:** Permite cadastrar e gerenciar as disciplinas e áreas do conhecimento conforme a BNCC, facilitando o planejamento pedagógico e o vínculo com habilidades e códigos.
 - **Funcionalidades:** Cadastro, edição, vínculo com códigos BNCC, busca e relatórios.

- **Categorias CID-10**
 - **Ícone:** categorias médicas (`fas fa-layer-group` ou similar)
 - **Objetivo:** Permite gerenciar as categorias da Classificação Internacional de Doenças (CID-10), organizando as condições médicas em grupos padronizados.
 - **Funcionalidades:** Cadastro, edição, consulta, busca e vínculo com condições CID-10.

- **Condições CID-10**
 - **Ícone:** condição médica (`fas fa-notes-medical` ou similar)
 - **Objetivo:** Permite gerenciar as condições e diagnósticos médicos conforme a CID-10, permitindo o registro detalhado de laudos e condições de saúde dos alunos/pacientes.
 - **Funcionalidades:** Cadastro, edição, busca, anexos e vínculo com alunos/pacientes.

- **Metas/Habilidades (PDI)**
 - **Ícone:** alvo ou estrela (`fas fa-bullseye`, `fas fa-star`)
 - **Objetivo:** Permite cadastrar, definir, acompanhar e avaliar metas e habilidades estabelecidas no PDI e PAEE de cada aluno/paciente.
 - **Funcionalidades:** Cadastro e edição de metas/habilidades, acompanhamento do progresso, relatórios e exportação de dados.

- **Usuários**
 - **Ícone:** usuário administrativo (`fas fa-user-shield` ou similar)
 - **Objetivo:** Permite cadastrar novos usuários para acesso, gerenciar contas, atribuir permissões, papéis e acessar informações de login e perfil.
 - **Funcionalidades:** Cadastro, edição, redefinição de senha, atribuição de grupos/permissões, ativação/desativação de contas e consulta de histórico de acesso.

- **Profissionais**
 - **Ícone:** usuário profissional (`fas fa-user-md` ou similar)
 - **Objetivo:** Gerenciar a equipe multidisciplinar, incluindo cadastro, especialidades, agenda e vínculo com alunos/pacientes.
 - **Funcionalidades:** Cadastro, agenda, especialidades, permissões e relatórios de atuação.

- **Escolas**
 - **Ícone:** escola (`fas fa-school`)
 - **Objetivo:** Permite gerenciar e cadastrar escolas públicas, parceiras, turmas e profissionais da educação e saúde dos alunos/pacientes com as instituições de ensino.
 - **Funcionalidades:** Cadastro de escolas, turmas, professores, histórico escolar e relatórios educacionais.

- **Mensagens**
 - **Ícone:** balão de conversa (`fas fa-comments`)
 - **Objetivo:** Centralizar a comunicação entre usuários do sistema, permitindo o envio e recebimento de mensagens em tempo real.
 - **Funcionalidades:** Envio/recebimento de mensagens, notificações, busca de conversas, organização por tópicos/grupos e integração com notificações do sistema.

- **Configurações**
 - **Ícone:** engrenagem (`fas fa-cog`)
 - **Objetivo:** Permite inserir e acessar as informações da Prefeitura, como logomarca, cnpj, endereço e dados dos gestores, que serão usados nos relatórios.
 - **Funcionalidades:** Gerenciamento de permissões, parâmetros do sistema, integrações, personalização de módulos e manutenção de dados.

*Obs.: Os módulos exibidos podem variar conforme as permissões do usuário e as configurações do sistema.*

---

## 2. Menu do Usuário (Navbar)

### Notificações
- **Ícone:** sino (`fas fa-bell`)
- **Objetivo:** Exibe os alertas de novas mensagens e permite acesso rápido a notificações recentes.

### Menu do Usuário
- **Ícone:** usuário (`fas fa-user-circle`)
- **Objetivo:** Permite o acesso às opções de perfil, alteração de senha e logout. Exibe o nome do usuário autenticado e permite a personalização de dados pessoais.

---

## Observações Gerais

- Os menus do sidebar podem variar conforme as permissões do usuário e as configurações do sistema.
- Alguns itens podem ser exibidos ou ocultados conforme o contexto do usuário (ex: permissões de administrador, gestor, etc).
- Os ícones seguem o padrão FontAwesome, podendo ser customizados para cada módulo.
- Esta documentação deve ser revisada e atualizada sempre que houver alterações nos menus ou na estrutura do sistema.