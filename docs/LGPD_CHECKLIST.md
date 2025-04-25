# Checklist de Implementação LGPD – PIAWeb

Este checklist orienta as ações técnicas e organizacionais necessárias para garantir a conformidade da aplicação PIAWeb com a Lei Geral de Proteção de Dados (LGPD).

## 1. Base Legal e Responsabilidade
- [x] Registrar que a base legal do tratamento é a obrigação legal do município (art. 7º, II, LGPD). **(Já atendido, basta documentar na política/manual)**
- [x] Documentar que o município é o controlador dos dados. **(Já atendido, basta documentar na política/manual)**
- [x] Incluir na política/manual que o canal de atendimento ao titular é a prefeitura. **(Já atendido, basta documentar na política/manual)**

## 2. Segurança da Informação
- [x] Garantir HTTPS em todas as páginas. **(Já implementado)**
- [ ] Implementar criptografia de dados sensíveis em repouso (exemplo: django-encrypted-model-fields). **(A FAZER: definir campos e aplicar criptografia no banco de dados)**
- [ ] Garantir controle de acesso rigoroso (perfis, permissões Django). **(A FAZER: revisar e documentar a matriz de permissões, revisar perfis periodicamente)**
- [ ] Implementar autenticação de dois fatores (2FA) para administradores. **(A FAZER: instalar e configurar pacote de 2FA para Django)**
- [ ] Auditar e revisar permissões periodicamente. **(A FAZER: criar rotina/documentação de revisão periódica)**

## 3. Direitos dos Titulares
- [x] Garantir que os direitos possam ser exercidos via prefeitura. **(Já atendido, mas precisa ser documentado na política/manual)**
- [x] Incluir instrução clara na política/manual sobre como o titular pode solicitar acesso, correção ou exclusão de dados. **(Já atendido, basta documentar na política/manual)**

## 4. Compartilhamento de Dados
- [x] Confirmar que não há compartilhamento com terceiros. **(Já atendido, só documentar na política/manual)**
- [x] Documentar explicitamente essa ausência na política/manual. **(Já atendido, basta documentar na política/manual)**

## 5. Registro e Logs
- [x] Utilizar logs do Django para rastreabilidade. **(Já implementado)**
- [ ] Criar página interna restrita para consulta/auditoria de logs. **(A FAZER: desenvolver página de auditoria para administradores)**

## 6. Política de Privacidade e Termos de Uso
- [x] Redigir política de privacidade clara, incluindo:
  - Finalidade do tratamento
  - Base legal
  - Medidas de segurança
  - Canal para titulares
  - Ausência de compartilhamento
  **(Já atendido, basta documentar na política/manual)**
- [x] Disponibilizar política na página de apresentação e/ou dentro do sistema.
  **(Já atendido, basta documentar na política/manual)**

---

**Revisão sugerida a cada 12 meses ou em caso de atualização legal ou técnica relevante.**
