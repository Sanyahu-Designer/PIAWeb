# Documentação de Migração de Banco de Dados: MariaDB para PostgreSQL com Criptografia de Campos Sensíveis

## Objetivo
Orientar o processo de migração de dados de uma instância MariaDB (sem criptografia) para PostgreSQL, implementando criptografia de campos sensíveis conforme os novos requisitos de segurança e LGPD do sistema PIA.

---

## 1. Cenário Inicial
- Ambiente piloto utiliza MariaDB, sem criptografia de dados sensíveis.
- Nova aplicação utiliza PostgreSQL, com campos sensíveis criptografados via biblioteca (ex: django-cryptography).

---

## 2. Desafios Específicos
- Os dados em MariaDB estão em texto claro.
- Após migração, os campos sensíveis precisam ser criptografados no PostgreSQL.
- A criptografia é aplicada pelo Django ao salvar os registros, não durante a simples cópia dos dados.

---

## 3. Passos Detalhados da Migração

### 3.1. Exportação dos Dados do MariaDB
- Realize backup completo do banco MariaDB (ex: `mysqldump`).
- Alternativamente, utilize ferramentas Django para exportação (ex: `dumpdata`).

### 3.2. Importação Inicial no PostgreSQL
- Importe os dados para o PostgreSQL, mantendo o modelo antigo (sem criptografia) temporariamente.
- Ajuste tipos de dados e constraints conforme necessário.
- Valide a integridade dos dados importados.

### 3.3. Atualização dos Modelos para Campos Criptografados
- Atualize os modelos Django para utilizar campos criptografados (ex: `encrypt(models.CharField(...))`).
- Realize as migrações (`makemigrations` e `migrate`).

### 3.4. Regravação dos Dados Sensíveis (Aplicando Criptografia)
- Crie um script ou comando customizado Django para percorrer todos os registros e salvar novamente os campos sensíveis.
- Exemplo:

```python
from app.models import Aluno  # ajuste para o nome do seu app/model

for aluno in Aluno.objects.all():
    aluno.save()  # Isso faz o Django criptografar os campos sensíveis
```
- Repita para todos os modelos/campos sensíveis.

### 3.5. Validação e Testes
- Verifique se os dados sensíveis estão criptografados no banco PostgreSQL (valores não legíveis).
- Teste todas as funcionalidades do sistema (CRUD, buscas, relatórios).

### 3.6. Backup Final e Documentação
- Faça backup do banco já criptografado.
- Documente todo o processo para fins de auditoria LGPD.

---

## 4. Boas Práticas e Recomendações
- Realize a migração em ambiente de testes antes de executar em produção.
- Mantenha backups em todas as etapas.
- Documente eventuais problemas e soluções encontradas.
- Realize a migração fora do horário de uso do sistema.
- Valide os dados antes e depois da criptografia.

---

## 5. Observações Finais
- A criptografia de campos sensíveis é aplicada **apenas após** a regravação dos registros já no PostgreSQL.
- Campos que precisam ser pesquisados/ordenados não devem ser criptografados (ver checklist de criptografia).
- Ajuste scripts conforme a estrutura real dos seus modelos.

---

**Última atualização:** 29/04/2025
Responsável: 
