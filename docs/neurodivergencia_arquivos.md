# Arquivos Relacionados à Página de Neurodivergência

Este documento lista todos os arquivos relacionados à página de edição de neurodivergência, incluindo templates HTML, arquivos CSS e JavaScript que afetam sua aparência e funcionalidade.

## Arquivos HTML

### Templates principais
1. `/neurodivergentes/templates/admin/neurodivergentes/neurodivergencia/change_form.html` - Template principal para edição de neurodivergência
2. `/neurodivergentes/templates/admin/neurodivergentes/neurodivergencia/change_list_material_dashboard.html` - Template para listagem de neurodivergências

### Templates de diagnóstico (usados dentro da página de neurodivergência)
3. `/neurodivergentes/templates/admin/neurodivergentes/edit_inline/stacked_diagnostico.html` - Template para edição inline de diagnósticos
4. `/neurodivergentes/templates/admin/neurodivergentes/diagnostico_inline.html` - Template para diagnósticos em formato inline
5. `/neurodivergentes/templates/admin/neurodivergentes/diagnostico_stacked.html` - Template para diagnósticos em formato empilhado
6. `/neurodivergentes/templates/admin/neurodivergentes/diagnostico_stacked_custom.html` - Template personalizado para diagnósticos

## Arquivos CSS

### CSS específicos para neurodivergência
1. `/neurodivergentes/static/neurodivergentes/css/neurodivergentes_forms.css` - Estilos para formulários de neurodivergência
2. `/neurodivergentes/static/admin/css/neurodivergentes_forms.css` - Estilos para formulários de neurodivergência (admin)

### CSS para diagnósticos
3. `/neurodivergentes/static/neurodivergentes/css/diagnostico_add_button.css` - Estilos para botões de adicionar diagnóstico
4. `/neurodivergentes/static/neurodivergentes/css/diagnostico_button_fix.css` - Correções para botões de diagnóstico
5. `/neurodivergentes/static/neurodivergentes/css/diagnostico_field_fix.css` - Correções para campos de diagnóstico
6. `/neurodivergentes/static/neurodivergentes/css/diagnostico_inline_styles.css` - Estilos para diagnósticos inline
7. `/neurodivergentes/static/admin/css/diagnostico.css` - Estilos gerais para diagnósticos
8. `/neurodivergentes/static/admin/css/diagnostico_field_fix.css` - Correções para campos de diagnóstico (admin)
9. `/neurodivergentes/static/admin/css/field_overflow_fix.css` - Correções para overflow de campos

## Arquivos JavaScript

### JavaScript específicos para neurodivergência
1. `/neurodivergentes/static/admin/js/neurodivergentes_admin.js` - Funcionalidades admin para neurodivergência
2. `/neurodivergentes/static/js/neurodivergentes_admin.js` - Funcionalidades gerais para neurodivergência

### JavaScript para diagnósticos
3. `/neurodivergentes/static/neurodivergentes/js/diagnostico_buttons.js` - Funcionalidades para botões de diagnóstico
4. `/neurodivergentes/static/neurodivergentes/js/diagnostico_inline_fix.js` - Correções para diagnósticos inline
5. `/neurodivergentes/static/admin/js/diagnostico.js` - Funcionalidades gerais para diagnósticos
6. `/neurodivergentes/static/admin/js/categoria_condicao_filter.js` - Filtros para categorias e condições

## Problemas Conhecidos e Soluções

### Problema com o campo Neurodivergência (condicao)
O campo de Neurodivergência estava ultrapassando os limites da página devido a conflitos com a biblioteca Select2 que estava sobrescrevendo os estilos CSS.

### Soluções implementadas:
1. Adição de estilos CSS específicos para o campo de Neurodivergência em `diagnostico_field_fix.css`
2. Modificação do JavaScript em `diagnostico_buttons.js` para aplicar estilos específicos ao campo
3. Configuração de um intervalo para reaplicar os estilos periodicamente, garantindo que não sejam sobrescritos

### Arquivos-chave para resolver o problema:
- `/neurodivergentes/templates/admin/neurodivergentes/edit_inline/stacked_diagnostico.html`
- `/neurodivergentes/static/neurodivergentes/css/diagnostico_field_fix.css`
- `/neurodivergentes/static/admin/css/diagnostico_field_fix.css`
- `/neurodivergentes/static/neurodivergentes/js/diagnostico_buttons.js`
