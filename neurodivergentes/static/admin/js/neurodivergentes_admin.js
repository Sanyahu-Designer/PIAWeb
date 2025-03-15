document.addEventListener('DOMContentLoaded', function() {
    /**
     * Script para preencher automaticamente o campo categoria com base na condição selecionada
     * Isso permite que o usuário veja apenas o campo de condição, mas mantém a integridade do banco de dados
     */
    function setupAutoCategoriaFromCondicao() {
        // Mapeamento de condições para categorias
        const condicaoCategoriaMap = {};
        
        // Função para extrair a categoria do texto da condição
        function extractCategoriaFromText(text) {
            const match = text.match(/^([^:]+):/);
            return match ? match[1].trim() : null;
        }
        
        // Função para encontrar o ID da categoria com base no nome
        function findCategoriaIdByName(categoriaName, categoriaSelect) {
            for (let i = 0; i < categoriaSelect.options.length; i++) {
                const option = categoriaSelect.options[i];
                if (option.text.trim() === categoriaName) {
                    return option.value;
                }
            }
            return null;
        }
        
        // Processa todas as linhas do formulário
        function processFormRows() {
            // Procura todos os selects de condição
            document.querySelectorAll('select.condicao-select, select[name*="condicao"]').forEach(condicaoSelect => {
                // Encontra o campo de categoria correspondente
                let categoriaSelect;
                
                // Se estamos em uma linha de tabular inline
                if (condicaoSelect.name.includes('-')) {
                    const prefix = condicaoSelect.name.split('-condicao')[0];
                    categoriaSelect = document.querySelector(`select[name="${prefix}-categoria"]`);
                } 
                // Se estamos no formulário principal
                else {
                    const row = condicaoSelect.closest('.form-row, tr');
                    categoriaSelect = row.querySelector('select[name*="categoria"]');
                    if (!categoriaSelect) {
                        // Tenta encontrar no .form-row anterior
                        const prevRow = row.previousElementSibling;
                        if (prevRow) {
                            categoriaSelect = prevRow.querySelector('select[name*="categoria"]');
                        }
                    }
                }
                
                if (categoriaSelect) {
                    // Oculta o campo de categoria
                    const categoriaRow = categoriaSelect.closest('.form-row, td');
                    if (categoriaRow) {
                        categoriaRow.style.display = 'none';
                    }
                    
                    // Configura o evento de mudança para a condição
                    condicaoSelect.addEventListener('change', function() {
                        const selectedOption = condicaoSelect.options[condicaoSelect.selectedIndex];
                        if (selectedOption && selectedOption.value) {
                            const categoriaName = extractCategoriaFromText(selectedOption.text);
                            if (categoriaName) {
                                const categoriaId = findCategoriaIdByName(categoriaName, categoriaSelect);
                                if (categoriaId) {
                                    categoriaSelect.value = categoriaId;
                                }
                            }
                        }
                    });
                    
                    // Executa o evento de mudança inicialmente se já houver uma condição selecionada
                    if (condicaoSelect.value) {
                        const event = new Event('change');
                        condicaoSelect.dispatchEvent(event);
                    }
                }
            });
        }
        
        // Processa as linhas iniciais
        processFormRows();
        
        // Configura o observador para processar novas linhas adicionadas dinamicamente
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    // Aguarda um momento para que o DOM seja completamente atualizado
                    setTimeout(processFormRows, 100);
                }
            });
        });
        
        // Observa o documento para novos campos
        observer.observe(document.body, { childList: true, subtree: true });
    }
    
    // Inicializa o script
    setupAutoCategoriaFromCondicao();
    

    

    
    // Função para corrigir o formato de data do campo data_identificacao na aba Diagnóstico
    function fixDiagnosticoDateFormat() {
        // Seleciona todos os formulários de diagnóstico
        const diagnosticoForms = document.querySelectorAll('.diagnosticos-container form, .inline-related form, form');
        
        // Função para converter data do formato dd/mm/yyyy para yyyy-MM-dd
        function convertDateFormat(dateStr) {
            if (!dateStr) return '';
            
            // Verifica se a data já está no formato yyyy-MM-dd
            if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
                return dateStr;
            }
            
            // Converte de dd/mm/yyyy para yyyy-MM-dd
            const parts = dateStr.split('/');
            if (parts.length === 3) {
                const day = parts[0].padStart(2, '0');
                const month = parts[1].padStart(2, '0');
                const year = parts[2];
                return `${year}-${month}-${day}`;
            }
            
            return dateStr;
        }
        
        // Função para exibir data no formato brasileiro
        function formatDateForDisplay(input) {
            // Adiciona um placeholder para indicar o formato esperado
            input.setAttribute('placeholder', 'dd/mm/aaaa');
            
            // Se o navegador não suportar o tipo date, usar texto simples
            if (input.type !== 'date') {
                input.type = 'text';
            }
        }
        
        diagnosticoForms.forEach(form => {
            // Procura especificamente pelo campo data_identificacao ou qualquer campo de data
            const dateFields = form.querySelectorAll('input[type="date"], input[name*="data_identificacao"], input[name*="data_diagnostico"]');
            
            dateFields.forEach(field => {
                // Adiciona log para verificar se o campo está sendo processado
                console.log("Campo de data encontrado: " + field.name);

                // Formata o campo para exibição
                formatDateForDisplay(field);
                
                // Adiciona evento para converter o formato quando o campo perde o foco
                field.addEventListener('blur', function() {
                    if (this.value && this.value.includes('/')) {
                        this.value = convertDateFormat(this.value);
                    }
                });
                
                // Adiciona evento para converter o formato antes do envio do formulário
                if (form && !form._dateSubmitListenerAdded) {
                    form.addEventListener('submit', function(e) {
                        const dateInputs = this.querySelectorAll('input[type="date"], input[name*="data_identificacao"], input[name*="data_diagnostico"]');
                        dateInputs.forEach(input => {
                            if (input.value && input.value.includes('/')) {
                                input.value = convertDateFormat(input.value);
                            }
                        });
                    });
                    form._dateSubmitListenerAdded = true;
                }
            });
        });
        
        // Observa mudanças no DOM para processar campos adicionados dinamicamente
        const observer = new MutationObserver(function(mutations) {
            let needsProcessing = false;
            
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    needsProcessing = true;
                }
            });
            
            if (needsProcessing) {
                const newDateFields = document.querySelectorAll('input[type="date"], input[name*="data_identificacao"], input[name*="data_diagnostico"]');
                newDateFields.forEach(field => {
                    if (!field._dateEventAdded) {
                        formatDateForDisplay(field);
                        
                        field.addEventListener('blur', function() {
                            if (this.value && this.value.includes('/')) {
                                this.value = convertDateFormat(this.value);
                            }
                        });
                        
                        field._dateEventAdded = true;
                    }
                });
            }
        });
        
        // Observa o documento inteiro para alterações nos campos de data
        observer.observe(document.body, { childList: true, subtree: true });
    }
    
    // Executa a função de correção de formato de data
    fixDiagnosticoDateFormat();
    console.log("Função fixDiagnosticoDateFormat executada");

    // Adiciona cabeçalhos às seções
    const sections = {
        'tab-dados-pessoais': 'Dados Pessoais',
        'tab-localizacao': 'Localização',
        'tab-endereco': 'Endereço',
        'tab-contato': 'Contato',
        'tab-nascimento': 'Nascimento e Primeira Infância',
        'tab-medico': 'Informações Médicas',
        'tab-historico': 'Histórico',
        'tab-relacionamentos': 'Relacionamentos',
        'tab-desenvolvimento': 'Desenvolvimento',
        'tab-percepcao': 'Percepção dos Responsáveis'
    };

    Object.entries(sections).forEach(([className, title]) => {
        const section = document.querySelector(`.${className}`);
        if (section) {
            const header = document.createElement('div');
            header.className = 'tab-header';
            header.textContent = title;
            section.insertBefore(header, section.firstChild);
        }
    });

    // Inicializa máscaras para campos formatados
    if (typeof jQuery !== 'undefined') {
        jQuery(function($) {
            // Verifica se a função mask está disponível antes de usá-la
            if (typeof $.fn.mask === 'function') {
                try {
                    // Máscara para celular
                    $('#id_celular').mask('(00) 00000-0000', {
                        onKeyPress: function(phone, e, field, options) {
                            const masks = ['(00) 00000-0000'];
                            const mask = masks[0];
                            $('#id_celular').mask(mask, options);
                        }
                    });
                    
                    // Máscara para CEP
                    $('#id_cep').mask('00000-000');

                    // Máscaras adicionais
                    $('[data-mask]').each(function() {
                        $(this).mask($(this).attr('data-mask'));
                    });

                    // Adiciona log para verificar se o plugin jQuery Mask foi inicializado
                    console.log("jQuery Mask plugin inicializado corretamente");
                } catch (e) {
                    console.warn('Erro ao aplicar máscaras:', e);
                }
            } else {
                console.warn('jQuery Mask plugin não está disponível');
            }
        });
    }

    // CEP auto-complete com tratamento de erro
    const cepInput = document.querySelector('#id_cep');
    if (cepInput) {
        cepInput.addEventListener('blur', function() {
            const cep = this.value.replace(/\D/g, '');
            if (cep.length === 8) {
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
                        document.querySelector('#id_endereco').value = data.logradouro || '';
                        document.querySelector('#id_bairro').value = data.bairro || '';
                        document.querySelector('#id_cidade').value = data.localidade || '';
                        
                        // Seleciona o estado correto
                        const estadoSelect = document.querySelector('#id_estado');
                        const estadoUF = data.uf.toUpperCase();
                        
                        for (let option of estadoSelect.options) {
                            if (option.value === estadoUF) {
                                option.selected = true;
                                break;
                            }
                        }
                        
                        estadoSelect.dispatchEvent(new Event('change'));
                    })
                    .catch(error => {
                        console.error('Erro ao consultar CEP:', error);
                        alert('Erro ao consultar o CEP. Por favor, tente novamente mais tarde.');
                    });
            }
        });
    }

    // Formatação automática do celular
    const celularInput = document.querySelector('#id_celular');
    if (celularInput) {
        celularInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length === 11) {
                this.value = `(${value.substr(0,2)}) ${value.substr(2,5)}-${value.substr(7)}`;
            }
        });
    }

    // Controle de campos dependentes
    function toggleDependentField(triggerField, dependentField) {
        const trigger = document.querySelector(triggerField);
        const dependent = document.querySelector(dependentField);
        
        if (trigger && dependent) {
            const parentDiv = dependent.closest('.form-row');
            
            function updateVisibility() {
                if (trigger.checked || trigger.value === 'True') {
                    parentDiv.classList.remove('hidden');
                } else {
                    parentDiv.classList.add('hidden');
                }
            }
            
            trigger.addEventListener('change', updateVisibility);
            updateVisibility();
        }
    }

    // Configura os campos dependentes
    toggleDependentField('#id_prematuridade', '#id_tempo_prematuridade');
    toggleDependentField('#id_convenio_medico', '#id_nome_convenio');
    toggleDependentField('#id_restricoes_alimentares', '#id_descricao_restricoes');

    // Formatação de JSON
    function formatJsonField(fieldId) {
        const field = document.querySelector(fieldId);
        if (field) {
            field.addEventListener('blur', function() {
                try {
                    const obj = JSON.parse(this.value);
                    this.value = JSON.stringify(obj, null, 2);
                } catch (e) {
                    // Mantém o valor original se não for JSON válido
                }
            });
        }
    }

    formatJsonField('#id_medicacoes_list');
    formatJsonField('#id_rotina_text');

    // Preview de imagem
    const fotoInput = document.querySelector('#id_foto_perfil');
    const previewImg = document.querySelector('.field-foto_preview img');
    
    if (fotoInput && previewImg) {
        fotoInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // Validação de campos numéricos
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach(input => {
        const min = input.getAttribute('min');
        const max = input.getAttribute('max');
        
        input.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (min && value < parseInt(min)) {
                this.value = min;
            }
            if (max && value > parseInt(max)) {
                this.value = max;
            }
        });
    });
});