window.addEventListener('load', function() {
    var $ = window.django ? django.jQuery : jQuery;

    // Função para reordenar as metas/habilidades
    function updateOrdem() {
        $('.meta-habilidade-inline tbody tr:not(.empty-form)').each(function(index) {
            $(this).find('input[name$="-ordem"]').val(index);
        });
    }

    // Adiciona botões de mover para cima/baixo em cada linha
    function addMoveButtons() {
        $('.meta-habilidade-inline tbody tr:not(.empty-form)').each(function() {
            if (!$(this).find('.move-buttons').length) {
                var buttons = $('<div class="move-buttons">' +
                    '<button type="button" class="move-up" title="Mover para cima">↑</button>' +
                    '<button type="button" class="move-down" title="Mover para baixo">↓</button>' +
                    '</div>');
                $(this).find('td:last').append(buttons);
            }
        });
    }

    // Handler para mover linha para cima
    $(document).on('click', '.move-up', function() {
        var row = $(this).closest('tr');
        var prev = row.prev('tr:not(.empty-form)');
        if (prev.length) {
            row.insertBefore(prev);
            updateOrdem();
        }
    });

    // Handler para mover linha para baixo
    $(document).on('click', '.move-down', function() {
        var row = $(this).closest('tr');
        var next = row.next('tr:not(.empty-form)');
        if (next.length) {
            row.insertAfter(next);
            updateOrdem();
        }
    });

    // Atualiza botões quando uma nova linha é adicionada
    $('.add-row a').click(function() {
        setTimeout(function() {
            addMoveButtons();
            updateOrdem();
        }, 100);
    });

    // Inicialização
    addMoveButtons();
    updateOrdem();
});