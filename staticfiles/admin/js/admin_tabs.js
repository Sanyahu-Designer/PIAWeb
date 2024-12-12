document.addEventListener('DOMContentLoaded', function() {
    // Adiciona cabeçalhos às seções
    const sections = {
        'tab-dados-pessoais': 'Dados Pessoais',
        'tab-endereco': 'Endereço',
        'tab-qualificacao': 'Qualificação Profissional',
        'tab-horarios': 'Horários de Atendimento',
        'tab-outros': 'Outros'
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

    // Inicializa as máscaras para os campos
    if (typeof jQuery !== 'undefined') {
        jQuery(function($) {
            $('[data-mask]').each(function() {
                $(this).mask($(this).attr('data-mask'));
            });
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
                        
                        document.querySelector('#id_endereco').value = data.logradouro || '';
                        document.querySelector('#id_bairro').value = data.bairro || '';
                        document.querySelector('#id_cidade').value = data.localidade || '';
                        
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

    // Carregamento de dados do usuário com tratamento de erro
    window.loadUserData = function(select) {
        const userId = select.value;
        if (userId) {
            fetch(`/profissionais/api/users/${userId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Usuário não encontrado');
                    }
                    return response.json();
                })
                .then(data => {
                    document.getElementById('id_first_name').value = data.first_name || '';
                    document.getElementById('id_last_name').value = data.last_name || '';
                    document.getElementById('id_email').value = data.email || '';
                })
                .catch(error => {
                    console.error('Erro ao carregar dados do usuário:', error);
                    alert('Erro ao carregar dados do usuário. Por favor, tente novamente.');
                    // Limpar campos em caso de erro
                    document.getElementById('id_first_name').value = '';
                    document.getElementById('id_last_name').value = '';
                    document.getElementById('id_email').value = '';
                });
        } else {
            // Limpar campos se nenhum usuário selecionado
            document.getElementById('id_first_name').value = '';
            document.getElementById('id_last_name').value = '';
            document.getElementById('id_email').value = '';
        }
    };
});