from django.urls import reverse
from django.utils.html import format_html

def get_view_button(self, obj):
    """
    Retorna o botão de visualização que leva para a lista de adaptações do aluno.
    """
    if not obj.aluno:
        return '-'
    url = f"{reverse('admin:adaptacao_curricular_adaptacaocurricularindividualizada_changelist')}?aluno__id__exact={obj.aluno.id}"
    return format_html(
        '<a href="{}" class="btn btn-outline-primary btn-sm mb-0 me-2" data-toggle="tooltip" data-original-title="Ver Adaptações">' 
        '<i class="material-symbols-rounded opacity-10" style="font-size: 16px;">visibility</i> Ver Adaptações</a>',
        url
    )

def get_acoes(self, obj):
    """
    Retorna os botões de ação para a lista de adaptações do aluno.
    """
    edit_url = reverse('admin:adaptacao_curricular_adaptacaocurricularindividualizada_change', args=[obj.id])
    delete_url = reverse('admin:adaptacao_curricular_adaptacaocurricularindividualizada_delete', args=[obj.id])
    return format_html(
        '<div class="ms-auto">' 
        '<a href="{}" class="btn btn-outline-primary btn-sm mb-0 me-2" data-toggle="tooltip" data-original-title="Editar">' 
        '<i class="material-symbols-rounded opacity-10" style="font-size: 16px;">edit</i> Editar</a>' 
        '<a href="{}" class="btn btn-outline-danger btn-sm mb-0" data-toggle="tooltip" data-original-title="Remover">' 
        '<i class="material-symbols-rounded opacity-10" style="font-size: 16px;">delete</i> Remover</a>' 
        '</div>',
        edit_url, delete_url
    )
