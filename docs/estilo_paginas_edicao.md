# Documentação: Padronização de Estilos nas Páginas de Edição

## Visão Geral

Este documento descreve a implementação da padronização de estilos nas páginas de edição do sistema PIA, com foco especial nos campos Select2 e no layout de duas colunas. A solução foi implementada inicialmente na página de edição do PDI (Plano de Desenvolvimento Individual) e deve ser replicada para outras páginas de edição.

## Problema

As páginas de edição do sistema apresentavam inconsistências visuais, especialmente:

1. Campos Select2 (como Aluno/Paciente e Pedagogo Responsável) com botões de ação indesejados
2. Layout desalinhado, com campos e labels mal posicionados
3. Falta de consistência visual entre as diferentes páginas de edição
4. Formato inadequado do cabeçalho, mostrando informações desnecessárias como a data
5. Botões de ação (Salvar, Salvar e continuar) sem o estilo visual padrão do sistema

## Solução Implementada

### 1. Criação de Templates Específicos

Para cada modelo que necessita de personalização, criamos um template específico que estende o template padrão `admin/change_form_standard.html`. Por exemplo:

```
/templates/admin/neurodivergentes/pdi/change_form.html
```

### 2. Estrutura do Template

O template personalizado segue esta estrutura:

```html
{% extends "admin/change_form_standard.html" %}
{% load i18n admin_urls static %}

{% block extrastyle %}{{ block.super }}
<style>
  /* Estilos específicos para a página */
</style>
{% endblock %}

{% block field_sets %}
  <!-- Estrutura personalizada para os campos -->
{% endblock %}

{% block inline_field_sets %}
  <!-- Estrutura personalizada para os inlines -->
{% endblock %}

{% block extrajs %}{{ block.super }}
<script>
  // JavaScript específico para a página
</script>
{% endblock %}
```

### 3. Layout de Duas Colunas

O layout de duas colunas é implementado usando o sistema de grid do Bootstrap, que já está incluído no template padrão. A estrutura básica é:

```html
<div class="row">
  {% for line in fieldset %}
    {% for field in line %}
      <div class="col-md-6 mb-3">
        <!-- Conteúdo do campo -->
      </div>
    {% endfor %}
  {% endfor %}
</div>
```

Para campos que devem ocupar a linha inteira (como áreas de texto), adicionamos classes específicas:

```css
.field-observacoes .col-md-6,
.field-descricao .col-md-6,
.field-conclusao .col-md-6,
.field-diario_de_classe .col-md-6 {
  flex: 0 0 100% !important;
  max-width: 100% !important;
}
```

### 4. Estilização dos Campos Select2

Os campos Select2 (como Aluno/Paciente e Pedagogo Responsável) recebem estilos específicos para garantir a aparência correta:

```css
/* Estilos para os campos Select2 */
.select2-container--default .select2-selection--single,
.select2-container--default .select2-selection--multiple {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  min-height: 38px !important;
  padding: 0.25rem 0.5rem !important;
}

.select2-container--default .select2-selection--single .select2-selection__rendered {
  line-height: 36px;
  padding-left: 0.5rem;
}

/* Remover seta para baixo */
.select2-container--default .select2-selection--single .select2-selection__arrow {
  display: none !important;
}

/* Remover botão X para limpar */
.select2-container--default .select2-selection--single .select2-selection__clear {
  display: none !important;
}

/* Garantir que o Select2 no campo específico tenha o estilo correto */
.field-neurodivergente .select2-container {
  width: 100% !important;
}

.field-neurodivergente .select2-selection,
.field-pedagogo_responsavel .select2-selection {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  min-height: 38px !important;
  padding: 0.25rem 0.5rem !important;
}
```

### 5. Ocultação de Botões de Ação

Para ocultar os botões de ação (editar, incluir, visualizar) nos campos relacionados, usamos CSS e JavaScript:

```css
/* Ocultar botões de ação nos campos relacionados */
.field-neurodivergente .related-widget-wrapper-link,
.field-pedagogo_responsavel .related-widget-wrapper-link,
.field-neurodivergente .related-lookup,
.field-pedagogo_responsavel .related-lookup {
  display: none !important;
}
```

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // Garantir que os botões de ação nos campos relacionados estejam ocultos
  const hideRelatedButtons = function() {
    const relatedButtons = document.querySelectorAll('.field-neurodivergente .related-widget-wrapper-link, .field-pedagogo_responsavel .related-widget-wrapper-link, .field-neurodivergente .related-lookup, .field-pedagogo_responsavel .related-lookup');
    relatedButtons.forEach(button => {
      button.style.display = 'none';
    });
  };
  
  // Executar imediatamente e também após um pequeno atraso para garantir que funcione
  hideRelatedButtons();
  setTimeout(hideRelatedButtons, 500);
});
```

### 6. Personalização do Cabeçalho

Para modificar o formato do cabeçalho de "PDI de João Silva - 2025-01-08" para "PDI - João Silva", utilizamos JavaScript para modificar o DOM após o carregamento da página:

```javascript
document.addEventListener('DOMContentLoaded', function() {
  // Modificar o título da página
  if (!document.querySelector('body.add-form')) {
    const titleElement = document.querySelector('.card-header .shadow-dark h6');
    if (titleElement) {
      // Obter o nome do neurodivergente
      const neurodivergenteName = document.querySelector('#id_neurodivergente').selectedOptions[0].text;
      if (neurodivergenteName) {
        titleElement.textContent = 'PDI - ' + neurodivergenteName;
      }
    }
  }
});
```

Esta abordagem tem várias vantagens:
- Funciona independentemente da estrutura do template base
- É executada no lado do cliente, então não depende de modificações no backend
- Mantém a formatação visual consistente com o resto da interface
- Mostra dinamicamente o nome do aluno/paciente específico que está sendo editado

### 7. Estilização dos Botões de Ação (Salvar)

Para garantir que o botão Salvar tenha a aparência correta (fundo rosa #e91e63), existem duas abordagens:

#### 7.1. Sobrescrever o bloco `submit_buttons_bottom`

Uma opção é sobrescrever o bloco `submit_buttons_bottom` e definir diretamente a classe `btn-primary` para o botão:

```html
{% block submit_buttons_bottom %}
  <div class="submit-row d-flex justify-content-between mt-4">
    <div class="d-flex gap-2">
      {% if show_save %}
        <button type="submit" class="btn btn-primary mb-0" name="_save">
          <i class="material-symbols-rounded opacity-10" style="font-size: 16px;">save</i> {% translate 'Salvar' %}
        </button>
      {% endif %}
      <!-- Outros botões... -->
    </div>
  </div>
{% endblock %}
```

#### 7.2. Usar CSS para estilizar o botão (Recomendado)

A abordagem mais flexível é manter a estrutura HTML original do template base, mas sobrescrever o estilo do botão usando CSS específico:

```css
/* Estilo para o botão Salvar */
.submit-row .btn-outline-primary,
.submit-row button[name="_save"] {
  color: #fff !important;
  background-color: #e91e63 !important;
  border-color: #e91e63 !important;
  box-shadow: 0 3px 3px 0 rgba(233, 30, 99, 0.15), 0 3px 1px -2px rgba(233, 30, 99, 0.2), 0 1px 5px 0 rgba(233, 30, 99, 0.15) !important;
}

.submit-row .btn-outline-primary:hover,
.submit-row button[name="_save"]:hover {
  background-color: #d81b60 !important;
  border-color: #c2185b !important;
  box-shadow: 0 14px 26px -12px rgba(233, 30, 99, 0.4), 0 4px 23px 0 rgba(0, 0, 0, 0.12), 0 8px 10px -5px rgba(233, 30, 99, 0.2) !important;
}
```

Esta abordagem tem várias vantagens:
- Funciona independentemente da classe aplicada ao botão no HTML
- Não requer modificação da estrutura do template base
- Mantém a consistência visual mesmo se o template base for atualizado
- Usa seletores CSS específicos que têm maior prioridade

## Arquivos Relevantes

1. **Template Padrão:**
   - `/templates/admin/change_form_standard.html`

2. **Estilos Globais:**
   - `/static/admin/css/form_fields_style.css`
   - `/static/admin/css/select2_custom.css`

3. **JavaScript para Select2:**
   - `/static/admin/js/select2_initializer.js`

4. **Templates Específicos:**
   - `/templates/admin/neurodivergentes/pdi/change_form.html`
   - `/templates/admin/neurodivergentes/monitoramento/change_form.html`
   - (Outros templates específicos a serem criados)

## Como Replicar para Outras Páginas

Para aplicar este padrão a outras páginas de edição:

1. Crie um novo template na pasta `/templates/admin/[app]/[modelo]/change_form.html`
2. Estenda o template padrão `admin/change_form_standard.html`
3. Copie e adapte os blocos `extrastyle`, `field_sets`, `inline_field_sets` e `extrajs`
4. Ajuste os seletores CSS e JavaScript para os campos específicos do modelo
5. Teste a página para garantir que todos os elementos estejam corretamente estilizados

## Considerações Importantes

- Os estilos específicos devem ser incluídos no bloco `extrastyle` para garantir que tenham prioridade sobre os estilos globais
- O JavaScript deve ser incluído no bloco `extrajs` e deve ser executado após o carregamento da página
- Para campos que devem ocupar a linha inteira, adicione classes específicas no CSS
- Teste em diferentes tamanhos de tela para garantir que o layout responsivo funcione corretamente
- Verifique se os botões de ação estão corretamente estilizados, especialmente o botão Salvar que deve ter o fundo rosa (#e91e63)
