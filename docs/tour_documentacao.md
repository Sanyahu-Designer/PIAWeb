# Documentação do Tour Interativo do Sistema PIA

## Objetivo
Implementar um tour interativo guiado para facilitar a navegação e entendimento das principais funcionalidades do dashboard e menus do sistema PIA.

---

## Arquivos Criados

- **static/js/tour.js**
  - Script principal do tour. Responsável por:
    - Definir os passos do tour (menus, gráficos, cards, tabelas, etc.)
    - Gerenciar a navegação entre etapas
    - Adicionar o botão "Fazer Tour" na interface (sidebar)
    - Garantir responsividade e integração com o layout

- **templates/admin/tour_btn_fix.html** (opcional)
  - Ponto de inserção customizado para o botão do tour, caso necessário.

- **docs/tour_documentacao.md**
  - Este arquivo de documentação.

---

## Arquivos Alterados

- **templates/admin/base.html**
  - Inclusão do script do tour:
    ```html
    <script src="{% static 'js/tour.js' %}"></script>
    ```

- **templates/admin/base_material.html**
  - Inclusão do script do tour:
    ```html
    <script src="{% static 'js/tour.js' %}"></script>
    ```

- **staticfiles/js/tour.js** / **staticfiles/js/pia_tour.js** / **staticfiles/css/pia_tour.css**
  - (Se utilizados pelo seu fluxo de build ou deploy, podem ser versões minificadas ou auxiliares.)

---

## Principais Funcionalidades do Tour
- Passos guiados para todos os menus e gráficos do dashboard.
- Botão "Fazer Tour" posicionado como botão flutuante no canto inferior direito, abaixo do botão de notificação.
- Responsividade: o botão acompanha o layout e não sobrepõe elementos essenciais.
- Textos explicativos e navegação intuitiva.

---

## Observações
- O tour pode ser expandido facilmente: basta adicionar novos passos no array `tourSteps` do arquivo `static/js/tour.js`.
- O botão "Fazer Tour" é inserido diretamente na sidebar para garantir alinhamento e padrão visual.
- Caso o container da sidebar não seja encontrado, o botão é adicionado ao `body` como fallback.

---

## Manutenção
- Para alterar textos, ordem ou elementos do tour, edite o array `tourSteps` em `static/js/tour.js`.
- Para mudar o posicionamento do botão, ajuste a lógica de inserção no mesmo arquivo.
- Sempre confira se o script está incluído nos templates base.

---

## Histórico de Alterações
- [x] Criação do tour.js
- [x] Inclusão do script nos templates base
- [x] Ajuste do botão "Fazer Tour" na sidebar
- [x] Documentação criada em `docs/tour_documentacao.md`

---

**Dúvidas ou melhorias:**
Entre em contato com a equipe de desenvolvimento ou consulte este documento para manutenção futura.
