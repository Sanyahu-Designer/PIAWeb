# Implementação do Campo de Anexos

## Objetivo
Melhorar a experiência de upload de arquivos no sistema PIA, com foco em usabilidade e design.

## Características Principais

### Design Visual
- Utilização de card com estilo Material Dashboard
- Fundo desfocado (blur)
- Sombra suave
- Margem inferior para separação

### Funcionalidades
- Input de arquivo personalizado
- Exibição apenas do nome do arquivo
- Ícone de upload com estilo consistente
- Texto de ajuda explicativo

## Código HTML

```html
<div class="card card-body blur shadow-blur mb-4">
  <div class="form-group">
    <h6 class="text-dark mb-3">
      Anexar Documentos Complementares
      <span class="text-muted" style="font-size: 0.7em; margin-left: 5px;">(opcional)</span>
    </h6>
    <div class="input-group input-group-outline">
      <!-- Input de arquivo oculto -->
      <input 
        type="file" 
        class="form-control" 
        id="{{ field.field.id_for_label }}" 
        name="{{ field.field.name }}"
        style="opacity: 0; position: absolute; z-index: -1;"
      >
      <!-- Ícone de upload -->
      <div class="input-group-prepend">
        <span class="input-group-text bg-gradient-primary">
          <i class="material-symbols-rounded text-white">upload_file</i>
        </span>
      </div>
      <!-- Input de texto para exibição -->
      <input 
        type="text" 
        class="form-control" 
        placeholder="Selecionar Arquivo" 
        readonly 
        style="background-color: #f8f9fa; cursor: pointer;"
        onclick="document.getElementById('{{ field.field.id_for_label }}').click();"
        id="{{ field.field.id_for_label }}_display"
      >
    </div>
    <small class="form-text text-muted mt-2">
      Você pode anexar documentos como relatórios, laudos ou outros documentos relevantes para complementar o parecer.
    </small>
  </div>
</div>
```

## JavaScript para Manipulação

```javascript
document.addEventListener('DOMContentLoaded', function() {
  var fileInput = document.getElementById('{{ field.field.id_for_label }}');
  var displayInput = document.getElementById('{{ field.field.id_for_label }}_display');
  
  // Configurar valor inicial se existir
  {% if field.field.initial %}
    var initialFileName = '{{ field.field.initial.name }}'.split('/').pop().split('\\').pop();
    displayInput.value = initialFileName;
  {% endif %}

  fileInput.addEventListener('change', function() {
    var fileName = this.value.split('\\').pop().split('/').pop();
    displayInput.value = fileName ? fileName : 'Selecionar Arquivo';
  });
});
```

## Problemas Resolvidos
- Exibição do caminho completo do arquivo
- Falta de estilo visual atraente
- Experiência de usuário pouco intuitiva

## Melhorias
- Design responsivo
- Feedback visual claro
- Extração correta do nome do arquivo
- Consistência com o design do Material Dashboard

## Considerações Futuras
- Validação de tipos de arquivo
- Limite de tamanho de upload
- Suporte para múltiplos arquivos
