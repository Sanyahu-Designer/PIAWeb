# Documentação do Card Grupo Familiar

## Elementos Visuais

### 1. Estrutura do Card
- **Cabeçalho**: Gradiente cinza (`linear-gradient(to right, #6c757d, #8d99ae)`) com título em branco
- **Posicionamento elevado**: Classes `position-relative mt-n4 mx-3 z-index-2`
- **Sombra e bordas arredondadas**: Classes `shadow-dark border-radius-lg`
- **Corpo do card**: Padding interno de 3 unidades (`p-3`)
- **Rodapé**: Centralizado com padding de 2 unidades (`p-2 text-center`)

### 2. Grid Layout
- Layout responsivo com 3 colunas em telas grandes, 2 em tablets e 1 em dispositivos móveis
- Classes: `col-12 col-md-6 col-lg-4` para cada item
- Espaçamento entre itens: `g-3` (grid gap)
- Container principal: `.grupo-familiar-grid`

### 3. Botão "Adicionar Membro Familiar"
- Classe: `btn btn-outline-primary btn-sm`
- Ícone: `material-symbols-rounded opacity-10` com tamanho de 20px
- Posicionamento: Centralizado abaixo do grid (`text-center`)
- Transição suave ao passar o mouse: `transition: all 0.2s ease`
- Efeito hover: Texto branco, fundo escuro (#344767)

### 4. Botão "Excluir"
- Classe: `btn btn-sm btn-outline-danger delete-button w-100`
- Ícone: `material-symbols-rounded` com tamanho de 16px
- Posicionamento: Rodapé do card, largura total
- Efeito hover: Fundo vermelho (#f44336), texto branco

### 5. Estilo para Itens Marcados para Exclusão
- Opacidade reduzida: `opacity: 0.6`
- Borda tracejada vermelha: `border: 2px dashed #f44336`
- Fundo levemente avermelhado: `background-color: #fff5f5`

### 6. Campos do Formulário
- Labels com estilo consistente
- Campos com bordas arredondadas: `border-radius: 0.5rem`
- Campos com classe: `form-control form-control-sm`
- Campos importantes com classe adicional: `required-field`

## Funcionalidades JavaScript

### 1. Inicialização
```javascript
function initGrupoFamiliar() {
  // Aplica estilos aos campos
  styleFormFields();
  
  // Configura os botões de exclusão existentes
  setupDeleteButtons();
  
  // Configura o botão de adicionar membro
  setupAddButton();
  
  // Configura a validação do formulário
  setupFormValidation();
}
```

### 2. Botão "Adicionar Membro Familiar"
```javascript
function setupAddButton() {
  $('#{{ inline_admin_formset.formset.prefix }}-add-button').off('click').on('click', function(e) {
    e.preventDefault();
    
    // Obtém o número total de formulários atual
    const totalForms = parseInt($('#id_{{ inline_admin_formset.formset.prefix }}-TOTAL_FORMS').val());
    
    // Cria o HTML para o novo membro
    const newMemberHtml = `
      <div class="w-100 mb-4 grupo-familiar-item">
        <div class="inline-related" id="{{ inline_admin_formset.formset.prefix }}-${totalForms}">
          <div class="card h-100 shadow-sm">
            <!-- Estrutura do card com cabeçalho, corpo e rodapé -->
          </div>
        </div>
      </div>
    `;
    
    // Adiciona o novo membro ao grid
    $('.grupo-familiar-grid').append(newMemberHtml);
    
    // Incrementa o contador de formulários
    $('#id_{{ inline_admin_formset.formset.prefix }}-TOTAL_FORMS').val(totalForms + 1);
    
    // Configura o botão de exclusão do novo membro
    setupDeleteButtons();
  });
}
```

### 3. Botão "Excluir"
```javascript
function setupDeleteButtons() {
  // Primeiro, vamos garantir que os checkboxes de exclusão estão visíveis para debug
  $('.delete-row').css('display', 'none');
  
  // Marca cards já excluídos com estilo visual
  $('.delete-row input[type="checkbox"]:checked').each(function() {
    $(this).closest('.grupo-familiar-item').addClass('marked-for-deletion');
    const $button = $(this).closest('.grupo-familiar-item').find('.delete-button');
    $button.html('<i class="material-symbols-rounded" style="font-size: 16px;">restore</i> Restaurar');
  });
  
  // Adiciona evento para os botões de exclusão
  $('.delete-button').off('click').on('click', function() {
    const $item = $(this).closest('.grupo-familiar-item');
    const $deleteCheckbox = $item.find('.delete-row input[type="checkbox"]');
    
    if ($deleteCheckbox.is(':checked')) {
      // Restaurar o item
      $deleteCheckbox.prop('checked', false);
      $item.removeClass('marked-for-deletion');
      $(this).html('<i class="material-symbols-rounded" style="font-size: 16px;">delete</i> Excluir');
    } else {
      // Marcar para exclusão
      $deleteCheckbox.prop('checked', true);
      $item.addClass('marked-for-deletion');
      $(this).html('<i class="material-symbols-rounded" style="font-size: 16px;">restore</i> Restaurar');
    }
  });
}
```

### 4. Estilização dos Campos
```javascript
function styleFormFields() {
  // Aplica classes Bootstrap aos campos
  $('#{{ inline_admin_formset.formset.prefix }}-group select').addClass('form-control form-control-sm');
  $('#{{ inline_admin_formset.formset.prefix }}-group input[type="text"]').addClass('form-control form-control-sm');
  $('#{{ inline_admin_formset.formset.prefix }}-group input[type="date"]').addClass('form-control form-control-sm');
  
  // Remove validação obrigatória do lado do cliente
  $('#{{ inline_admin_formset.formset.prefix }}-group input').removeAttr('required');
  
  // Destaca campos importantes visualmente
  $('#{{ inline_admin_formset.formset.prefix }}-group input[name$="-nome"]').addClass('required-field');
  $('#{{ inline_admin_formset.formset.prefix }}-group input[name$="-data_nascimento"]').addClass('required-field');
}
```

### 5. CSS Completo
```css
/* Estilos para o layout vertical */
.grupo-familiar-grid {
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* Correção para o cabeçalho */
.card-header {
  margin-bottom: 0;
  position: relative;
}

/* Estilo para o cabeçalho com gradiente */
.shadow-dark {
  background: linear-gradient(to right, #6c757d, #8d99ae) !important;
}

/* Estilo para o botão de exclusão */
.delete-button {
  transition: all 0.2s ease;
  border-radius: 0.25rem;
}

.delete-button:hover {
  background-color: #f44336;
  color: white;
  border-color: #f44336;
}

/* Estilo para o botão de adicionar */
.add-button {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.add-button:hover {
  background-color: #344767;
  color: white;
  border-color: #344767;
}

/* Estilo para itens marcados para exclusão */
.marked-for-deletion {
  opacity: 0.6;
  position: relative;
}

.marked-for-deletion .card {
  border: 2px dashed #f44336 !important;
  background-color: #fff5f5;
}

/* Estilos responsivos */
@media (min-width: 768px) {
  .grupo-familiar-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
}

@media (min-width: 992px) {
  .grupo-familiar-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## HTML Estrutural

```html
<div class="fieldset-container mb-4">
  <h5 class="text-dark mb-3">
    <i class="material-symbols-rounded opacity-10 me-2">people</i>
    {{ inline_admin_formset.opts.verbose_name_plural|capfirst }}
  </h5>
  
  {{ inline_admin_formset.formset.management_form }}
  {{ inline_admin_formset.formset.non_form_errors }}
  
  <div class="js-inline-admin-formset inline-group" id="{{ inline_admin_formset.formset.prefix }}-group"
     data-inline-type="stacked"
     data-inline-formset="{{ inline_admin_formset.inline_formset_data }}">
    
    <div class="grupo-familiar-container">
      <div class="grupo-familiar-grid">
        {% for inline_admin_form in inline_admin_formset %}
          <div class="{% if not forloop.last %}w-100{% else %}empty-form d-none{% endif %} mb-4 grupo-familiar-item">
            <div class="inline-related{% if forloop.last and inline_admin_formset.has_add_permission %} empty-form{% endif %}"
                 id="{{ inline_admin_formset.formset.prefix }}-{% if not forloop.last %}{{ forloop.counter0 }}{% else %}empty{% endif %}">
              
              {% if not forloop.last %}
                <div class="card h-100 shadow-sm">
                  <!-- Cabeçalho do card -->
                  <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                    <div class="shadow-dark border-radius-lg pt-4 pb-3">
                      <h6 class="text-white text-capitalize ps-3">Membro #{{ forloop.counter }}</h6>
                    </div>
                  </div>
                  
                  <!-- Corpo do card -->
                  <div class="card-body p-3">
                    <!-- Campos do formulário -->
                  </div>
                  
                  <!-- Rodapé do card -->
                  <div class="card-footer p-2 text-center">
                    <button type="button" class="btn btn-sm btn-outline-danger delete-button w-100">
                      <i class="material-symbols-rounded" style="font-size: 16px;">delete</i> Excluir
                    </button>
                  </div>
                </div>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </div>
      
      <!-- Botão para adicionar novo membro -->
      <div class="add-row mt-3 text-center">
        <button type="button" class="btn btn-outline-primary btn-sm add-button" id="{{ inline_admin_formset.formset.prefix }}-add-button">
          <i class="material-symbols-rounded opacity-10" style="font-size: 20px;">add</i>
          <span>Adicionar Membro Familiar</span>
        </button>
      </div>
    </div>
  </div>
</div>
```

Esta documentação contém todos os detalhes de estilo e funcionalidade do card Grupo Familiar, que poderão ser utilizados como referência para implementações futuras.
