# Documentação: Correção do Card Diagnósticos

Esta documentação descreve o processo de correção dos problemas encontrados no card Diagnósticos da página de edição de Neurodivergências, aplicando a mesma abordagem usada para corrigir o card Grupo Familiar.

## Problemas Identificados

1. **Campo Neurodivergência não clicável**: O campo de seleção não estava funcionando corretamente.
2. **Erro ao salvar novos diagnósticos**: Problemas de validação impediam o salvamento correto.
3. **Erro ao substituir neurodivergência**: Validação rígida entre categoria e condição causava erros.
4. **Problemas de estilo**: Inconsistências visuais com o restante do sistema.

## Solução Implementada

### 1. Criação de um Novo Template

Criamos um novo template baseado no padrão do Django Admin para stacked inlines:

```html
{% load i18n admin_urls %}
<div class="js-inline-admin-formset inline-group"
     id="{{ inline_admin_formset.formset.prefix }}-group"
     data-inline-type="stacked"
     data-inline-formset="{{ inline_admin_formset.inline_formset_data }}">
<fieldset class="module {{ inline_admin_formset.classes }}">
  <h2>{{ inline_admin_formset.opts.verbose_name_plural|capfirst }}</h2>
  {{ inline_admin_formset.formset.management_form }}
  {{ inline_admin_formset.formset.non_form_errors }}

  {% for inline_admin_form in inline_admin_formset %}
    <div class="inline-related{% if inline_admin_form.original or inline_admin_form.show_url %} has_original{% endif %}{% if forloop.last and inline_admin_formset.has_add_permission %} empty-form last-related{% endif %}" id="{{ inline_admin_formset.formset.prefix }}-{% if not forloop.last %}{{ forloop.counter0 }}{% else %}empty{% endif %}">
      <h3>
        <b>{{ inline_admin_formset.opts.verbose_name|capfirst }}:</b>
        <span class="inline_label">{% if inline_admin_form.original %}{{ inline_admin_form.original }}{% else %}#{{ forloop.counter }}{% endif %}</span>
        {% if inline_admin_formset.formset.can_delete and inline_admin_form.original %}
          <span class="delete">{{ inline_admin_form.deletion_field.field }} {{ inline_admin_form.deletion_field.label_tag }}</span>
        {% endif %}
      </h3>
      {% if inline_admin_form.form.non_field_errors %}{{ inline_admin_form.form.non_field_errors }}{% endif %}
      {% for fieldset in inline_admin_form %}
        {% include "admin/includes/fieldset.html" %}
      {% endfor %}
      {% if inline_admin_form.needs_explicit_pk_field %}{{ inline_admin_form.pk_field.field }}{% endif %}
      {% if inline_admin_form.fk_field %}{{ inline_admin_form.fk_field.field }}{% endif %}
    </div>
  {% endfor %}
</fieldset>
</div>
```

### 2. Adição de Script para Garantir Campos Select Clicáveis

Adicionamos um script no template para garantir que os campos select sejam clicáveis:

```html
<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    // Função para configurar os selects
    function setupSelects() {
      // Seleciona todos os selects
      const selects = document.querySelectorAll('select[name*="condicao"]');
      
      selects.forEach(function(select) {
        // Adiciona classes para estilização consistente
        select.classList.add('form-control');
        
        // Garante que o select seja clicável
        select.style.pointerEvents = 'auto';
        select.style.cursor = 'pointer';
        
        // Garante que o select tenha a aparência correta
        select.style.border = '1px solid #d2d6da';
        select.style.borderRadius = '0.5rem';
        select.style.minHeight = '38px';
        select.style.padding = '0.25rem 0.5rem';
        select.style.width = '100%';
        select.style.backgroundColor = '#fff';
        select.style.appearance = 'auto';
        select.style.webkitAppearance = 'auto';
        select.style.mozAppearance = 'auto';
      });
    }
    
    // Configura os selects iniciais
    setupSelects();
    
    // Configura os selects quando novos formulários são adicionados
    const addButton = document.querySelector('.add-row a');
    if (addButton) {
      addButton.addEventListener('click', function() {
        setTimeout(setupSelects, 100);
      });
    }
  });
</script>
```

### 3. Criação de Arquivos CSS e JavaScript Específicos

Criamos arquivos CSS e JavaScript específicos para o card Diagnósticos:

**CSS (diagnostico.css)**:
```css
/* Estilos para os campos select */
select[name*="condicao"] {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  min-height: 38px !important;
  padding: 0.25rem 0.5rem !important;
  width: 100% !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  background-color: #fff !important;
  appearance: auto !important;
  -webkit-appearance: auto !important;
  -moz-appearance: auto !important;
}

/* Estilos para os campos de data */
input[name*="data_identificacao"] {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  min-height: 38px !important;
  padding: 0.25rem 0.5rem !important;
  width: 100% !important;
}

/* Estilos para os campos de texto */
textarea[name*="observacoes"] {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  padding: 0.25rem 0.5rem !important;
  width: 100% !important;
  min-height: 80px !important;
}
```

**JavaScript (diagnostico.js)**:
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Função para formatar as datas no carregamento inicial
    function formatInitialDates() {
        document.querySelectorAll('input[name*="data_identificacao"]').forEach(function(input) {
            if (input.value) {
                // Garante que a data está no formato correto para o input type="date"
                const date = new Date(input.value);
                if (!isNaN(date.getTime())) {
                    input.value = date.toISOString().split('T')[0];
                }
            }
        });
    }
    
    // Função para garantir que os selects funcionem corretamente
    function setupSelects() {
        // Seleciona todos os selects de condição
        const condicaoSelects = document.querySelectorAll('select[name*="condicao"]');
        
        condicaoSelects.forEach(function(select) {
            // Adiciona classes para estilização consistente
            select.classList.add('form-control');
            
            // Garante que o select seja clicável
            select.style.pointerEvents = 'auto';
            select.style.cursor = 'pointer';
        });
    }

    // Formata as datas existentes
    formatInitialDates();
    
    // Configura os selects
    setupSelects();

    // Observa mudanças na DOM para lidar com linhas adicionadas dinamicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                setTimeout(function() {
                    formatInitialDates();
                    setupSelects();
                }, 100);
            }
        });
    });
});
```

### 4. Modificação da Classe DiagnosticoInline

Modificamos a classe DiagnosticoInline no arquivo admin.py:

```python
class DiagnosticoInline(admin.StackedInline):
    model = DiagnosticoNeurodivergente
    form = DiagnosticoNeurodivergenteForms
    extra = 1
    min_num = 0
    can_delete = True
    verbose_name = 'Diagnóstico'
    verbose_name_plural = 'Diagnósticos'
    template = 'admin/neurodivergentes/edit_inline/stacked_diagnostico.html'
    
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={
            'class': 'vDateField form-control', 
            'type': 'date'
        })},
        models.TextField: {'widget': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        })},
        models.CharField: {'widget': forms.TextInput(attrs={
            'class': 'form-control'
        })}
    }
    
    fields = (
        ('data_identificacao',),
        ('condicao',),
        ('observacoes',)
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'condicao':
            # Organiza as condições por categoria para melhor visualização
            condicoes = CondicaoNeurodivergente.objects.all().order_by('categoria__nome', 'nome')
            kwargs['queryset'] = condicoes
            kwargs['widget'] = forms.Select(attrs={
                'class': 'form-control'
            })
            # Remove a validação de categoria para permitir a seleção de qualquer condição
            kwargs['to_field_name'] = 'id'
        elif db_field.name == 'categoria':
            # Torna o campo categoria não obrigatório para evitar problemas de validação
            kwargs['required'] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {
            'all': ('admin/css/diagnostico.css',)
        }
        js = ('admin/js/diagnostico.js',)
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        class CustomFormset(formset):
            def _construct_form(self, *args, **kwargs):
                form = super()._construct_form(*args, **kwargs)
                if form.instance and form.instance.data_identificacao:
                    form.initial['data_identificacao'] = form.instance.data_identificacao.strftime('%Y-%m-%d')
                return form
                
            def save_new(self, form, commit=True):
                """
                Sobrescreve o método save_new para garantir que novos diagnósticos
                sejam corretamente salvos no banco de dados.
                """
                obj = super().save_new(form, commit=False)
                
                # Garante que a categoria seja definida com base na condição
                if obj.condicao_id and not obj.categoria_id:
                    obj.categoria = obj.condicao.categoria
                
                if commit:
                    obj.save()
                return obj
        
        return CustomFormset
```

### 5. Modificação do Modelo DiagnosticoNeurodivergente

Modificamos o método clean do modelo DiagnosticoNeurodivergente para tornar a validação mais flexível:

```python
def clean(self):
    # Garante que a categoria seja definida com base na condição
    if self.condicao_id and not self.categoria_id:
        self.categoria = self.condicao.categoria
        
    # Verifica se a condição pertence à categoria apenas se ambos estiverem definidos
    # e se a categoria não for None
    if (self.condicao_id and self.categoria_id and 
        self.condicao.categoria_id != self.categoria_id and
        self.categoria is not None):
        # Em vez de lançar um erro, ajustamos a categoria para corresponder à condição
        self.categoria = self.condicao.categoria
```

## Princípios Gerais para Correção de Problemas Similares

Para corrigir problemas similares em outros cards do sistema, siga estes princípios:

1. **Utilize os templates padrão do Django Admin**: Sempre que possível, baseie-se nos templates padrão do Django Admin e faça apenas as modificações necessárias.

2. **Simplifique a validação**: Torne a validação mais flexível para evitar erros ao salvar, especialmente em campos relacionados.

3. **Garanta que os selects sejam clicáveis**: Adicione estilos e JavaScript para garantir que os campos select sejam clicáveis e funcionem corretamente.

4. **Sobrescreva o método save_new**: Garanta que os novos itens sejam salvos corretamente, preenchendo campos relacionados quando necessário.

5. **Mantenha a consistência visual**: Utilize os estilos padrão do sistema para manter a consistência visual em todas as páginas.

6. **Teste todas as funcionalidades**: Após fazer as alterações, teste todas as funcionalidades para garantir que estão funcionando corretamente.

## Aplicando em Outros Cards

Para aplicar estas correções em outros cards com problemas similares:

1. Identifique o template personalizado que está sendo usado
2. Crie um novo template baseado no padrão do Django Admin
3. Crie arquivos CSS e JavaScript específicos para o card
4. Modifique a classe Inline no arquivo admin.py
5. Ajuste a validação no modelo relacionado
6. Teste todas as funcionalidades

Seguindo estes passos, você poderá corrigir problemas similares em outros cards do sistema, mantendo a consistência visual e garantindo o funcionamento correto de todas as funcionalidades.
