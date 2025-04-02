# Guia de Padronização das Páginas de Edição

Este documento descreve como implementar o padrão visual em todas as páginas de edição do sistema, seguindo o modelo estabelecido para a página de Alunos/Pacientes.

## Arquivos Criados

1. **CSS Centralizado**: `/static/admin/css/edit_form_standard.css`
   - Contém todos os estilos necessários para padronizar as páginas de edição
   - Inclui os estilos dos menus suspensos (Select2)

2. **Template Base**: `/templates/admin/change_form_standard.html`
   - Template base que todas as páginas de edição devem estender
   - Implementa a estrutura padrão e os scripts necessários

## Como Implementar em uma Página

Para padronizar uma página de edição, siga estes passos:

### 1. Modificar o Template da Página

Substitua:
```html
{% extends "admin/change_form_material.html" %}
```

Por:
```html
{% extends "admin/change_form_standard.html" %}
```

### 2. Remover Estilos Duplicados

- Remova qualquer link para `form_fields_style.css` pois já está incluído no template base
- Mantenha apenas os estilos específicos necessários para a página em questão

### 3. Ajustar o Breadcrumb (se necessário)

Mantenha o bloco de breadcrumb específico para cada página:

```html
{% block breadcrumbs %}
<nav aria-label="breadcrumb">
  <ol class="breadcrumb bg-transparent mb-0 pb-0 pt-1 px-0 me-sm-6 me-5">
    <li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="{% url 'admin:index' %}">{% translate 'Home' %}</a></li>
    <li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="{% url 'admin:app_list' app_label='app_name' %}">App Name</a></li>
    <li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="{% url 'admin:app_name_model_name_changelist' %}">{{ opts.verbose_name_plural|capfirst }}</a></li>
    <li class="breadcrumb-item text-sm text-dark active" aria-current="page">
      {% if add %}{% blocktranslate with name=opts.verbose_name %}Adicionar {{ name }}{% endblocktranslate %}
      {% else %}{{ original|truncatewords:"18" }}
      {% endif %}
    </li>
  </ol>
</nav>
{% endblock %}
```

### 4. Manter Blocos Específicos (se necessário)

Se a página tiver blocos específicos como `field_sets` ou `inline_field_sets` personalizados, mantenha-os conforme necessário.

## Exemplo de Implementação

Aqui está um exemplo de como implementar o padrão em uma página:

```html
{% extends "admin/change_form_standard.html" %}
{% load i18n admin_urls static %}

{% block extrastyle %}{{ block.super }}
<!-- Apenas estilos específicos para esta página -->
<style>
  /* Estilos específicos aqui */
</style>
{% endblock %}

{% block breadcrumbs %}
<!-- Breadcrumb específico para esta página -->
{% endblock %}

{% block field_sets %}
<!-- Se precisar personalizar o layout dos campos -->
{% endblock %}
```

## Características do Padrão Visual

### Menus Suspensos (Select2)

Os menus suspensos seguem estas características:
- Bordas arredondadas (border-radius: 0.5rem)
- Altura adequada (min-height: 38px)
- Sem seta para baixo e sem botão X para limpar
- Cor rosa (#e91e63) para o contorno e foco
- Cores neutras dentro do menu suspenso
- Mensagens em português

### Campos de Formulário

- Bordas arredondadas
- Efeito de foco com contorno rosa
- Indicação clara para campos obrigatórios (asterisco vermelho)
- Textos de ajuda formatados com estilo sutil

### Botões

- Estilo outline para botões de ação
- Ícones do Material Symbols
- Efeitos de hover com elevação suave

## Lista de Páginas a Padronizar

- [x] Anamnese
- [x] Registro de Evolução
- [ ] Neurodivergência
- [ ] Adaptação Curricular Individualizada
- [ ] PDI
- [ ] Parecer
- [ ] Escola
- [ ] Profissional
- [ ] Meta/Habilidade
- [ ] Categoria CID-10
- [ ] Condição CID-10
- [ ] Código BNCC
- [ ] Disciplina BNCC
