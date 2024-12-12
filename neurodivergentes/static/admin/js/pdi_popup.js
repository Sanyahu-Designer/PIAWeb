document.addEventListener('DOMContentLoaded', function() {
    // Adiciona evento de clique para todos os botões de visualizar PDI
    document.querySelectorAll('.view-pdi-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const pdiId = this.dataset.pdiId;
            loadPDIDetails(pdiId);
        });
    });
});

function loadPDIDetails(pdiId) {
    // Remover popup existente se houver
    const existingPopup = document.querySelector('.pdi-popup');
    if (existingPopup) {
        existingPopup.remove();
    }

    // Criar container do popup
    const popupContainer = document.createElement('div');
    popupContainer.className = 'pdi-popup';
    popupContainer.style.display = 'flex';
    
    // Carregar conteúdo via AJAX
    fetch(`/neurodivergentes/pdi/${pdiId}/popup/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados do PDI');
            }
            return response.text();
        })
        .then(html => {
            popupContainer.innerHTML = html;
            document.body.appendChild(popupContainer);
            
            // Adicionar eventos de fechamento
            const closeBtn = popupContainer.querySelector('.close-popup');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    popupContainer.remove();
                });
            }
            
            popupContainer.addEventListener('click', (e) => {
                if (e.target === popupContainer) {
                    popupContainer.remove();
                }
            });
        })
        .catch(error => {
            // Apenas loga o erro no console, sem mostrar alerta
            console.error('Erro:', error);
        });
}