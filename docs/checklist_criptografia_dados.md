# Checklist de Criptografia de Dados Sensíveis em Repouso

Este documento tem como objetivo acompanhar a implementação da criptografia de dados sensíveis em repouso no sistema PIA, conforme exigido pela LGPD e boas práticas de segurança.

## Checklist de Modelos para Criptografia de Dados

- [x] Aluno/Paciente
- [x] Profissional
- [x] Grupo Familiar
- [x] Cliente (Prefeitura)
- [x] Escola
- [x] Usuário
- [x] Anamnese
- [x] Registro de Evolução
- [x] PDI (Plano de Desenvolvimento Individual)
- [x] PEI (Plano Educacional Individualizado)
- [x] PAEE (Plano de Atendimento Educacional Especializado)
- [x] Parecer

> Use este checklist para garantir que todos os modelos relevantes tenham seus campos sensíveis revisados e, se necessário, criptografados conforme a LGPD.

## Critérios Gerais
- **Criptografar:** Dados que, se vazados, representam alto risco ao titular e NÃO são usados para buscas, ordenações ou filtros frequentes.
- **Não criptografar:** Dados necessários para buscas, ordenações, relatórios ou integração com outros sistemas.

## 1. Modelos e Campos Sensíveis
Marque os campos à medida que forem criptografados e testados.

### Aluno/Paciente
**Criptografar:**
- [x] CPF
- [x] RG
- [x] CEP
- [x] Endereço
- [x] Número
- [x] Complemento
- [x] Bairro
- [x] Cidade
- [x] Estado
- [x] Celular
- [x] E-mail

**Não criptografar:**
- Nome completo (usado em buscas, relatórios e exibição)
- Código CID (usado em relatórios, estatísticas e buscas)
- Matrícula, número de prontuário, código interno
- Gênero, escolaridade, tipo de vínculo

### Profissional
**Criptografar:**
- [x] CPF, RG, registro profissional
- [x] Endereço residencial
- [x] Telefone/Celular pessoal

**Não criptografar:**
- Nome completo
- Área de atuação, especialidade, cargo

### Grupo Familiar
**Criptografar:**
- [x] Documentos dos membros (caso armazenados)
- [x] Dados de contato pessoais (caso armazenados)

**Nota:**
No momento, o modelo GrupoFamiliar não armazena campos sensíveis/documentos ou contato pessoal. Caso futuramente sejam necessários, implementar criptografia conforme padrão dos demais modelos.

**Não criptografar:**
- Nome dos membros (caso seja necessário para busca ou exibição em relatórios)

### Cliente (Prefeitura)
**Criptografar:**
- [x] Contatos dos secretários municipais (e-mail e telefone)
- [x] Dados de responsável financeiro: CPF, telefone, e-mail pessoal

**Não criptografar:**
- Nome da prefeitura, CNPJ, inscrição estadual (usados em relatórios fiscais e buscas)
- Endereço institucional
- Nome dos secretários e autoridades

### Relatórios, Anexos e Evoluções
**Criptografar:**
- [x] Arquivos anexos (laudos, exames, relatórios médicos)
- [x] Campos de observação/síntese confidencial em relatórios de evolução, anamnese, PDI/PEI

**Não criptografar:**
- Títulos dos relatórios, datas, códigos de referência

## 2. Tarefas Técnicas Gerais
- [x] Escolher e configurar biblioteca de criptografia para Django
- [x] Implementar campos criptografados nos modelos
- [x] Ajustar views/forms para manipular dados criptografados
- [x] Garantir criptografia de backups e arquivos de mídia
- [x] Implementar e documentar gestão segura das chaves
- [x] Testar performance e integridade dos dados
- [x] Documentar justificativa para cada campo criptografado ou não (auditoria LGPD)

## 3. Observações/Notas
- Utilize este espaço para registrar decisões, dificuldades ou pontos de atenção durante a implementação.

---
Última atualização: 29/04/2025
Responsável: 
