# Implementação da Página de Edição de Código BNCC

## Visão Geral
Página de edição para o modelo `BNCCHabilidade`, com foco em padronização visual e experiência do usuário.

## Componentes Modificados

### Modelo (`models.py`)
- Método `__str__` simplificado para mostrar apenas disciplina e código
```python
def __str__(self):
    return f"{self.disciplina} - {self.codigo}"
```

### Admin (`admin.py`)
- Personalização do widget de seleção de disciplina
- Remoção de labels duplicados
```python
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    # Remover o label "Disciplina"
    if form.base_fields['disciplina'].label == 'Disciplina':
        form.base_fields['disciplina'].label = ''
    form.base_fields['disciplina'].widget = LabelAboveWidget(attrs={
        'class': 'select2-disciplina',
        'data-placeholder': 'Selecione a disciplina BNCC',
        'style': 'width: 100%; display: block;',
    })
    return form
```

### Widget Personalizado
- `LabelAboveWidget`: Remove labels e personaliza a renderização do campo Select
```python
class LabelAboveWidget(Select):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['data-hide-label'] = 'true'
        super().__init__(attrs=attrs)

    def render(self, name, value, attrs=None, renderer=None):
        select_html = super().render(name, value, attrs, renderer)
        html = f'''
        <div style="display: block; width: 100%;">
            <div style="display: block; width: 100%;">
                {select_html}
            </div>
        </div>
        '''
        return mark_safe(html)
```

## Padrões Aplicados
- Consistência visual com outros campos Select2
- Remoção de labels redundantes
- Placeholder personalizado
- Largura total do campo
- Estilo de seleção padronizado

## Próximos Passos
- Aplicar padrão similar em outros modelos com campos de seleção
- Revisar e padronizar widgets em toda a aplicação
