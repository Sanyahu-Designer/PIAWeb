django.jQuery(document).ready(function($) {
    // Configuração do Select2 para os campos de profissionais
    $('#id_profissionais_educacao').select2({
        theme: 'default',
        placeholder: 'Selecione os profissionais da educação...',
        allowClear: true,
        width: '100%',
        language: {
            noResults: function() {
                return "Nenhum profissional encontrado";
            }
        }
    });

    $('#id_profissionais_saude').select2({
        theme: 'default',
        placeholder: 'Selecione os profissionais da saúde...',
        allowClear: true,
        width: '100%',
        language: {
            noResults: function() {
                return "Nenhum profissional encontrado";
            }
        }
    });
});