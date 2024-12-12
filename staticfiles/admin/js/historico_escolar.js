django.jQuery(document).ready(function($) {
    // Agrupa as opções por categoria
    function groupSerieOptions() {
        const $select = $('#id_series_cursadas_from, #id_series_cursadas_to');
        
        $select.each(function() {
            const $options = $(this).find('option');
            const groups = {
                'EDUCAÇÃO INFANTIL': $('<optgroup label="Educação Infantil">'),
                'ENSINO FUNDAMENTAL I': $('<optgroup label="Ensino Fundamental I">'),
                'ENSINO FUNDAMENTAL II': $('<optgroup label="Ensino Fundamental II">')
            };
            
            $options.each(function() {
                const $option = $(this);
                const value = $option.val();
                
                // Determina a categoria baseada no valor
                let category;
                if (value.match(/^(bercario|maternal|jardim|pre)/)) {
                    category = 'EDUCAÇÃO INFANTIL';
                } else if (value.match(/^[1-5]ano/)) {
                    category = 'ENSINO FUNDAMENTAL I';
                } else {
                    category = 'ENSINO FUNDAMENTAL II';
                }
                
                groups[category].append($option.clone());
            });
            
            // Limpa e adiciona os grupos
            $(this).empty();
            Object.values(groups).forEach(group => {
                if (group.children().length) {
                    $(this).append(group);
                }
            });
        });
    }

    // Aplica o agrupamento inicial
    groupSerieOptions();

    // Reaplica o agrupamento após mover itens
    $('.selector-chooser button').click(function() {
        setTimeout(groupSerieOptions, 100);
    });

    // Mantém o agrupamento após filtrar
    $('.selector-filter input').on('input', function() {
        setTimeout(groupSerieOptions, 100);
    });
});