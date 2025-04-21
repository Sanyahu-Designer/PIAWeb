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
- Exibição de arquivo já anexado com botão para visualização/download
- Opção de excluir/limpar anexo já existente (checkbox destacado)
- Bloco de ações do anexo (visualizar/excluir) centralizado e dentro do card
- Checkbox maior, destacado na cor rosa, com marcador centralizado

## Código HTML Sugerido

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
      <!-- Campo somente leitura para exibir nome do arquivo -->
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
    <!-- Bloco de ações do anexo -->
    {% if field.field.initial %}
      <div class="d-flex align-items-center gap-3 mt-2" style="background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 0.5rem; padding: 0.5rem 1rem;">
        <a href="{{ field.field.initial.url }}" target="_blank" class="btn btn-outline-secondary btn-sm mb-0 d-flex align-items-center" style="height: 32px;">
          <i class="material-symbols-rounded opacity-10" style="font-size: 16px;">attach_file</i>
          <span class="ms-1">Ver anexo atual</span>
        </a>
        <div class="form-check mb-0 d-flex align-items-center" style="margin-left: 10px;">
          <input type="checkbox" name="{{ field.field.name }}-clear" id="id_{{ field.field.name }}_clear" class="form-check-input" style="width: 20px; height: 20px; accent-color: #e91e63; margin-top: 0; vertical-align: middle; box-shadow: none;">
          <label for="id_{{ field.field.name }}_clear" class="form-check-label ms-1 mb-0" style="color: #e91e63; font-weight: 500; cursor: pointer; margin-bottom: 0; white-space: nowrap;">
            Excluir anexo
          </label>
        </div>
      </div>
    {% endif %}
    <small class="form-text text-muted mt-2">
      Você pode anexar documentos como relatórios, laudos ou outros documentos relevantes para complementar o parecer.
    </small>
  </div>
</div>
```

## CSS Sugerido

```css
.form-check-input[type="checkbox"] {
  width: 20px;
  height: 20px;
  accent-color: #e91e63;
  margin-top: 0;
  vertical-align: middle;
  box-shadow: none;
}
.form-check-input[type="checkbox"]:focus {
  box-shadow: 0 0 0 0.15rem rgba(233,30,99,.25);
  border-color: #e91e63;
}
```

## Observações
- Para aplicar em outros campos de anexo, basta replicar o bloco HTML e CSS sugerido, ajustando os nomes dos campos conforme necessário.
- O padrão visual e de usabilidade deve ser mantido em todas as telas do sistema.
- Recomenda-se testar em diferentes navegadores e dispositivos para garantir responsividade e acessibilidade.

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

---

Atualizado em: 20/04/2025
Responsável: Equipe PIAWeb
