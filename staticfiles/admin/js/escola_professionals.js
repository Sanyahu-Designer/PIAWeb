django.jQuery(document).ready(function($) {
    // Função para estilizar os seletores de profissionais
    function setupProfessionalSelectors() {
        // Configuração para Profissionais da Educação
        const educacaoSelector = $('.field-profissionais_educacao .selector');
        if (educacaoSelector.length) {
            educacaoSelector.find('h2').each(function() {
                $(this).prepend('<i class="fas fa-graduation-cap" style="margin-right: 8px;"></i>');
            });
        }

        // Configuração para Profissionais da Saúde
        const saudeSelector = $('.field-profissionais_saude .selector');
        if (saudeSelector.length) {
            saudeSelector.find('h2').each(function() {
                $(this).prepend('<i class="fas fa-user-md" style="margin-right: 8px;"></i>');
            });
        }

        // Melhorar a experiência de seleção
        $('.selector select').on('mouseover', 'option', function() {
            $(this).css('background-color', '#f5f5f5');
        }).on('mouseout', 'option', function() {
            $(this).css('background-color', '');
        });

        // Adicionar tooltips aos botões
        $('.selector-chooser button').each(function() {
            const action = $(this).attr('title');
            $(this).tooltip({
                title: action,
                placement: 'right',
                container: 'body'
            });
        });

        // Melhorar a busca
        $('.selector-filter input').attr('placeholder', 'Digite para filtrar...')
            .on('input', function() {
                $(this).toggleClass('active-filter', $(this).val().length > 0);
            });
    }

    // Inicializar quando o DOM estiver pronto
    setupProfessionalSelectors();

    // Reinicializar quando houver mudanças dinâmicas
    $(document).on('formset:added', function() {
        setupProfessionalSelectors();
    });
});