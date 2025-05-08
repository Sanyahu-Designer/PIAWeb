# Documentação LGPD – PIAWeb

## 1. Contexto e Responsabilidade
A aplicação PIAWeb é de uso exclusivo das prefeituras municipais, para gestão pedagógica e psicossocial de alunos da rede pública. O município é o controlador dos dados pessoais, sendo responsável pelo cumprimento da LGPD.

## 2. Base Legal do Tratamento
O tratamento dos dados pessoais e sensíveis é realizado com base no art. 7º, inciso II, da LGPD – cumprimento de obrigação legal e regulatória pelo controlador (município). Não é necessário consentimento dos titulares para as finalidades do sistema.

## 3. Direitos dos Titulares
Os titulares (alunos, responsáveis, profissionais) podem exercer seus direitos (acesso, correção, exclusão, etc.) junto à prefeitura, por meio dos canais oficiais da Secretaria de Educação.

## 4. Segurança e Privacidade
- Todo acesso é restrito a usuários autorizados.
- O sistema utiliza HTTPS em todas as páginas.
- Dados sensíveis são criptografados em repouso.
- Autenticação em dois fatores (2FA) está habilitada para administradores.
- Logs de acesso e alterações são mantidos pelo sistema.

## 5. Compartilhamento de Dados
Os dados tratados na PIAWeb são de uso exclusivo da prefeitura. **Não há compartilhamento com terceiros.** Todos os titulares podem exercer seus direitos junto à Secretaria de Educação do município, utilizando os canais oficiais da Prefeitura.

## 6. Política de Privacidade (Texto-base)

> **Política de Privacidade – PIAWeb**
>
> Esta aplicação é destinada exclusivamente à gestão educacional municipal. Os dados pessoais tratados têm por finalidade o acompanhamento pedagógico e psicossocial dos alunos da rede pública, em cumprimento de obrigação legal do município.
>
> O acesso aos dados é restrito a usuários autorizados pela prefeitura. **Não há compartilhamento de dados com terceiros.** Os titulares podem exercer seus direitos junto à Secretaria de Educação do município, utilizando os canais oficiais da Prefeitura.
>
> A aplicação adota medidas técnicas e administrativas para proteção dos dados, incluindo controle de acesso, logs de operações e uso de HTTPS. Dados sensíveis são criptografados em repouso e autenticação em dois fatores está habilitada para administradores.
>
> Em caso de dúvidas ou solicitações, entre em contato com a Secretaria de Educação do seu município.
>
> Esta política será revisada a cada 12 meses ou em caso de atualização legal ou técnica relevante.

## 7. Disponibilização
Sugere-se disponibilizar a política de privacidade na página inicial da aplicação e/ou em área de fácil acesso dentro do sistema.

## 8. Checklist de Log de Auditoria LGPD

Para garantir conformidade com a LGPD e exigências governamentais, o log de auditoria do sistema PIAWeb deve atender aos seguintes requisitos:

### Ações que devem ser registradas
- Login/logout de usuários
- Troca de tenant (prefeitura)
- Criação, edição e exclusão de dados pessoais (alunos, profissionais, familiares, etc.)
- Alteração de permissões, grupos e configurações sensíveis
- Exportação/download de dados pessoais
- Visualização de dados sensíveis
- Tentativas de acesso não autorizado/falhas de autenticação

### Campos mínimos em cada linha do log
- Data e hora
- Usuário responsável (id, login, nome)
- IP de origem
- Tipo de ação (ex: create, update, delete, export, view, tenant_switch)
- Objeto afetado (ex: id do aluno, nome do arquivo exportado, tabela/modelo afetado)
- Valor anterior e novo (quando aplicável)
- Resultado da ação (sucesso/falha)

### Requisitos de segurança
- O log não pode ser alterado ou apagado por usuários comuns.
- Logs devem ser mantidos por tempo suficiente (ex: 5 anos).
- O acesso ao log deve ser restrito e auditável.

### Disponibilidade para auditoria
- Implementar (ou planejar) uma página interna para consulta dos logs, com filtros por usuário, ação, data etc.
- Documentar o procedimento para exportação dos logs em caso de auditoria.

### Checklist prático de conformidade do log de auditoria LGPD

- [x] Login/logout de usuários registrado
- [x] Troca de tenant (prefeitura) registrada
- [x] Criação de dados pessoais registrada
- [x] Edição de dados pessoais registrada
- [x] Exclusão de dados pessoais registrada
- [x] Alteração de permissões, grupos e configurações sensíveis registrada
- [x] Exportação/download de dados pessoais registrada
- [x] Visualização de dados sensíveis registrada
- [x] Tentativas de acesso não autorizado/falhas de autenticação registradas
- [x] Cada registro contém: data/hora, usuário, IP, tipo de ação, objeto afetado, valores anterior/novo (quando aplicável) e resultado
- [x] Log protegido contra alteração/remoção por usuários comuns
- [x] Logs mantidos por tempo suficiente (mínimo 5 anos)
- [x] Acesso ao log restrito e auditável
- [x] Página interna para consulta dos logs (planejada ou implementada)
- [x] Procedimento documentado para exportação dos logs em caso de auditoria

---

> **Observação:** O checklist acima deve ser revisado e atualizado periodicamente conforme evolução da legislação, exigências contratuais e melhores práticas de mercado.

---

**Última revisão: 25/04/2025**
