# Documentação: Correção do Card Grupo Familiar

Esta documentação descreve o processo de correção dos problemas encontrados no card Grupo Familiar do sistema PIA, incluindo a remoção de estilos com erros e a implementação correta mantendo os estilos padrão do sistema.

## Problemas Identificados

1. **Campo Vínculo/Parentesco não clicável**: O campo de seleção não estava funcionando corretamente, exibindo apenas um item e não permitindo interação.
2. **Novos membros não salvos**: Ao adicionar novos membros ao grupo familiar, os dados não eram persistidos no banco de dados.
3. **Erro ao salvar**: Erro relacionado ao campo `modified` que não existia no modelo Neurodivergente.
4. **Problemas de estilo**: Inconsistências visuais com o restante do sistema.

## Solução Implementada

### 1. Simplificação do Template

O primeiro passo foi substituir o template personalizado por um baseado no template padrão do Django Admin para stacked inlines:

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

Adicionamos um script diretamente no template para garantir que os campos select sejam clicáveis:

```html
<script type="text/javascript">
  document.addEventListener('DOMContentLoaded', function() {
    // Função para configurar os selects de vínculo
    function setupVinculoSelects() {
      // Seleciona todos os selects de vínculo
      const vinculoSelects = document.querySelectorAll('select[name*="vinculo"]');
      
      vinculoSelects.forEach(function(select) {
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
    setupVinculoSelects();
    
    // Configura os selects quando novos formulários são adicionados
    const addButton = document.querySelector('.add-row a');
    if (addButton) {
      addButton.addEventListener('click', function() {
        setTimeout(setupVinculoSelects, 100);
      });
    }
  });
</script>
```

### 3. Modificação do Arquivo CSS

Atualizamos o arquivo CSS para garantir que os campos de seleção tenham o estilo correto:

```css
/* Estilos para os campos select */
select[name*="vinculo"] {
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

select[name*="vinculo"]:focus {
  border-color: #e91e63 !important;
  outline: 0 !important;
  box-shadow: 0 0 0 0.2rem rgba(233, 30, 99, 0.25) !important;
}

/* Estilo para o botão de adicionar novo membro */
.add-row a {
  color: #e91e63 !important;
  border-color: #e91e63 !important;
  background-color: transparent !important;
  padding: 0.5rem 1rem !important;
  border-radius: 0.5rem !important;
  text-decoration: none !important;
  display: inline-block !important;
  margin-top: 1rem !important;
  border: 1px solid !important;
}

.add-row a:hover,
.add-row a:focus,
.add-row a:active {
  color: #d81557 !important;
  border-color: #d81557 !important;
  background-color: transparent !important;
  box-shadow: 0 3px 5px -1px rgba(233, 30, 99, 0.15) !important;
}

/* Estilos para os campos de formulário */
.form-row {
  margin-bottom: 1rem !important;
}

.form-row label {
  display: block !important;
  margin-bottom: 0.5rem !important;
  font-weight: 500 !important;
}

.form-row input[type="text"],
.form-row input[type="date"],
.form-row textarea {
  border: 1px solid #d2d6da !important;
  border-radius: 0.5rem !important;
  min-height: 38px !important;
  padding: 0.25rem 0.5rem !important;
  width: 100% !important;
}

.form-row input[type="text"]:focus,
.form-row input[type="date"]:focus,
.form-row textarea:focus {
  border-color: #e91e63 !important;
  outline: 0 !important;
  box-shadow: 0 0 0 0.2rem rgba(233, 30, 99, 0.25) !important;
}
```

### 4. Modificação do Arquivo JavaScript

Simplificamos o arquivo JavaScript para focar apenas nas funcionalidades essenciais:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Função para formatar as datas no carregamento inicial
    function formatInitialDates() {
        document.querySelectorAll('.date-input').forEach(function(input) {
            if (input.value) {
                // Garante que a data está no formato correto para o input type="date"
                const date = new Date(input.value);
                if (!isNaN(date.getTime())) {
                    input.value = date.toISOString().split('T')[0];
                }
            }
        });
    }
    
    // Função para garantir que os selects de vínculo funcionem corretamente
    function setupVinculoSelects() {
        // Seleciona todos os selects de vínculo
        const vinculoSelects = document.querySelectorAll('select[name*="vinculo"]');
        
        vinculoSelects.forEach(function(select) {
            // Adiciona classes para estilização consistente
            select.classList.add('form-control');
            
            // Garante que o select seja clicável
            select.style.pointerEvents = 'auto';
            select.style.cursor = 'pointer';
            
            // Adiciona evento de mudança para atualizar o campo outro_vinculo
            select.addEventListener('change', function() {
                const row = this.closest('.inline-related');
                const outroVinculoField = row.querySelector('input[name*="outro_vinculo"]');
                const outroVinculoContainer = outroVinculoField ? outroVinculoField.closest('.form-row') : null;
                
                if (outroVinculoContainer) {
                    if (this.value === 'outro') {
                        outroVinculoContainer.style.display = 'block';
                    } else {
                        outroVinculoContainer.style.display = 'none';
                    }
                }
            });
            
            // Dispara o evento change para configurar a visibilidade inicial
            select.dispatchEvent(new Event('change'));
        });
    }

    // Formata as datas existentes
    formatInitialDates();
    
    // Configura os selects de vínculo
    setupVinculoSelects();

    // Observa mudanças na DOM para lidar com linhas adicionadas dinamicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                setTimeout(function() {
                    formatInitialDates();
                    setupVinculoSelects();
                }, 100);
            }
        });
    });

    // Observa o container do inline formset
    const inlineContainer = document.querySelector('.inline-group');
    if (inlineContainer) {
        observer.observe(inlineContainer, {
            childList: true,
            subtree: true
        });
    }
});
```

### 5. Modificação da Classe GrupoFamiliarInline no admin.py

Atualizamos a classe GrupoFamiliarInline para garantir que o campo Vínculo/Parentesco seja renderizado corretamente:

```python
class GrupoFamiliarInline(admin.StackedInline):
    model = GrupoFamiliar
    extra = 1  # Permite adicionar pelo menos um novo membro por padrão
    template = 'admin/neurodivergentes/edit_inline/stacked_grupo_familiar.html'
    can_delete = True
    show_change_link = False
    
    formfield_overrides = {
        models.DateField: {
            'widget': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'vDateField date-input form-control',
                },
                format='%Y-%m-%d'
            )
        },
        models.CharField: {
            'widget': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        },
        models.TextField: {
            'widget': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            )
        }
    }
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        class CustomFormset(formset):
            def _construct_form(self, *args, **kwargs):
                form = super()._construct_form(*args, **kwargs)
                if form.instance and form.instance.data_nascimento:
                    form.initial['data_nascimento'] = form.instance.data_nascimento.strftime('%Y-%m-%d')
                return form
                
            def save_new(self, form, commit=True):
                """
                Sobrescreve o método save_new para garantir que novos membros
                sejam corretamente salvos no banco de dados.
                """
                obj = super().save_new(form, commit=False)
                if commit:
                    obj.save()
                return obj
        
        return CustomFormset
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Sobrescreve o método formfield_for_choice_field para garantir que
        o campo Vínculo/Parentesco tenha as opções corretas.
        """
        if db_field.name == 'vinculo':
            kwargs['widget'] = forms.Select(attrs={'class': 'form-control'})
            kwargs['choices'] = GrupoFamiliar.VINCULO_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    class Media:
        css = {
            'all': ('admin/css/grupo_familiar.css',)
        }
        js = ('admin/js/grupo_familiar.js',)
```

### 6. Correção do Modelo GrupoFamiliar

Corrigimos o modelo GrupoFamiliar para remover a referência ao campo `modified` que não existia:

```python
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # Se o neurodivergente existir, atualize-o
    if self.neurodivergente:
        # Apenas salva o neurodivergente, o campo updated_at será atualizado automaticamente
        self.neurodivergente.save()

# Sinais para atualizar o neurodivergente quando um membro do grupo familiar for salvo ou excluído
@receiver(post_save, sender=GrupoFamiliar)
def update_neurodivergente_on_save(sender, instance, **kwargs):
    if instance.neurodivergente:
        # Apenas salva o neurodivergente, o campo updated_at será atualizado automaticamente
        instance.neurodivergente.save()

@receiver(post_delete, sender=GrupoFamiliar)
def update_neurodivergente_on_delete(sender, instance, **kwargs):
    if instance.neurodivergente:
        # Apenas salva o neurodivergente, o campo updated_at será atualizado automaticamente
        instance.neurodivergente.save()
```

## Princípios Gerais para Correção de Problemas Similares

Para corrigir problemas similares em outras páginas do sistema, siga estes princípios:

1. **Utilize os templates padrão do Django Admin**: Sempre que possível, baseie-se nos templates padrão do Django Admin e faça apenas as modificações necessárias.

2. **Simplifique o JavaScript**: Mantenha o JavaScript focado apenas nas funcionalidades essenciais, evitando código desnecessário.

3. **Mantenha a consistência visual**: Utilize os estilos padrão do sistema para manter a consistência visual em todas as páginas.

4. **Verifique os modelos**: Certifique-se de que os modelos estão corretamente configurados e que as referências a campos inexistentes são removidas.

5. **Sobrescreva métodos específicos**: Em vez de reescrever completamente a funcionalidade, sobrescreva apenas os métodos específicos que precisam ser modificados.

6. **Adicione Media para recursos estáticos**: Utilize a classe Media para adicionar arquivos CSS e JavaScript específicos para cada inline ou admin.

7. **Teste todas as funcionalidades**: Após fazer as alterações, teste todas as funcionalidades para garantir que estão funcionando corretamente.

## Aplicando em Outras Páginas

Para aplicar estas correções em outras páginas com problemas similares:

1. Identifique o template personalizado que está sendo usado
2. Substitua pelo template padrão do Django Admin correspondente
3. Adicione os estilos CSS necessários para manter a consistência visual
4. Adicione o JavaScript necessário para garantir a funcionalidade correta
5. Verifique e corrija os modelos relacionados
6. Teste todas as funcionalidades

Seguindo estes passos, você poderá corrigir problemas similares em outras páginas do sistema, mantendo a consistência visual e garantindo o funcionamento correto de todas as funcionalidades.
