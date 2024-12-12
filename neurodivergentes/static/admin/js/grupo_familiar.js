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

    // Formata as datas existentes
    formatInitialDates();

    // Observa mudanças na DOM para lidar com linhas adicionadas dinamicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                formatInitialDates();
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