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

function showReportModal(event, url) {
    event.preventDefault();
    
    // Fecha qualquer modal aberto anteriormente
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.style.display = 'none';
    });
    
    // Abre o modal específico
    var modal = event.target.closest('a').nextElementSibling;
    modal.style.display = 'block';
    
    // Fecha o modal quando clicar fora dele
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
}

// Adiciona estilos CSS dinamicamente
var style = document.createElement('style');
style.textContent = `
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.4);
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    border-radius: 5px;
}

.modal-content h2 {
    margin-top: 0;
}

.modal-content form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.modal-content label {
    font-weight: bold;
}

.modal-content input[type="date"] {
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 3px;
}

.modal-content button {
    background-color: #79aec8;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

.modal-content button:hover {
    background-color: #417690;
}
`;
document.head.appendChild(style);