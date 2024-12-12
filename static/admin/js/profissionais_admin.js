document.addEventListener('DOMContentLoaded', function() {
    // CEP auto-complete aprimorado
    const cepInput = document.querySelector('#id_cep');
    if (cepInput) {
        cepInput.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
                // Adiciona classe de loading
                this.classList.add('loading');
                
                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Erro na consulta do CEP');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.erro) {
                            alert('CEP não encontrado. Por favor, verifique o número informado.');
                            return;
                        }
                        
                        // Preenche os campos com os dados do CEP
                        const campos = {
                            '#id_endereco': data.logradouro,
                            '#id_bairro': data.bairro,
                            '#id_cidade': data.localidade
                        };

                        Object.entries(campos).forEach(([selector, valor]) => {
                            const campo = document.querySelector(selector);
                            if (campo) {
                                campo.value = valor || '';
                                campo.dispatchEvent(new Event('change'));
                            }
                        });
                        
                        // Seleciona o estado
                        const estadoSelect = document.querySelector('#id_estado');
                        if (estadoSelect) {
                            const estadoUF = data.uf.toUpperCase();
                            for (let option of estadoSelect.options) {
                                if (option.value === estadoUF) {
                                    option.selected = true;
                                    estadoSelect.dispatchEvent(new Event('change'));
                                    break;
                                }
                            }
                        }
                    })
                    .catch(error => {
                        console.error('Erro ao consultar CEP:', error);
                        alert('Erro ao consultar o CEP. Por favor, tente novamente mais tarde.');
                    })
                    .finally(() => {
                        // Remove classe de loading
                        this.classList.remove('loading');
                    });
            }
        });
    }

    // Inicializa máscaras para campos formatados
    if (typeof jQuery !== 'undefined') {
        jQuery(function($) {
            $('[data-mask]').each(function() {
                $(this).mask($(this).attr('data-mask'));
            });
        });
    }

    // Inicializa select2 para campos de seleção
    if (typeof jQuery !== 'undefined' && typeof jQuery.fn.select2 !== 'undefined') {
        jQuery('#id_profissao').select2({
            theme: 'admin-select2',
            width: '100%'
        });
    }
});