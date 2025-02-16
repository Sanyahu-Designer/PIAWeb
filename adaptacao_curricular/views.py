from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration
from .models import AdaptacaoCurricularIndividualizada, BNCCDisciplina, AdaptacaoHabilidade

@login_required
def imprimir_adaptacao_disciplina(request, adaptacao_id, disciplina_id):
    """
    Gera um relatório PDF para todas as adaptações de uma disciplina específica.
    """
    # Busca a adaptação e a disciplina
    adaptacao = get_object_or_404(
        AdaptacaoCurricularIndividualizada.objects.select_related(
            'aluno',
            'escola',
            'profissional_responsavel'
        ),
        id=adaptacao_id
    )
    
    disciplina = get_object_or_404(BNCCDisciplina, id=disciplina_id)
    
    # Busca todas as adaptações de habilidade desta disciplina
    adaptacoes_habilidade = AdaptacaoHabilidade.objects.filter(
        aci=adaptacao,
        habilidade__disciplina=disciplina
    ).select_related(
        'habilidade'
    ).order_by(
        'habilidade__codigo',
        'habilidade__ano',
        'habilidade__trimestre'
    )
    
    # Prepara o contexto com todos os dados necessários
    context = {
        'adaptacao': adaptacao,
        'disciplina': disciplina,
        'adaptacoes_habilidade': adaptacoes_habilidade,
        'data_geracao': timezone.localtime(),
    }
    
    # Renderiza o template HTML
    html_string = render_to_string('admin/adaptacao_curricular/relatorio_disciplina.html', context)
    
    # Configura as fontes
    font_config = FontConfiguration()
    
    # Cria o PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(
        font_config=font_config,
        presentational_hints=True
    )
    
    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f'adaptacao_{adaptacao_id}_{disciplina.nome}.pdf'
    response['Content-Disposition'] = f'filename={filename}'
    
    return response
