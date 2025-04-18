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