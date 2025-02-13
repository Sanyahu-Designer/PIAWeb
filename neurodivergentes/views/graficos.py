from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from ..models import PDI, PDIMetaHabilidade, Neurodivergente
from datetime import datetime

@require_GET
def dados_graficos_parecer(request):
    """
    Retorna os dados para os gráficos do parecer avaliativo.
    Parâmetros esperados na URL:
    - aluno_id: ID do neurodivergente
    - data_inicio: Data inicial no formato YYYY-MM-DD
    - data_fim: Data final no formato YYYY-MM-DD
    """
    try:
        aluno_id = request.GET.get('aluno_id')
        data_inicio = datetime.strptime(request.GET.get('data_inicio'), '%Y-%m-%d').date()
        data_fim = datetime.strptime(request.GET.get('data_fim'), '%Y-%m-%d').date()

        # Dados para o gráfico de frequência
        pdis_concluidos = PDI.objects.filter(
            neurodivergente_id=aluno_id,
            status='concluido',
            data_criacao__range=(data_inicio, data_fim)
        ).annotate(
            mes=TruncMonth('data_criacao')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes')

        # Calcula a média de atendimentos
        media_atendimentos = pdis_concluidos.aggregate(
            media=Avg('total')
        )['media'] or 0

        # Dados para o gráfico de monitoramento
        metas_habilidades = PDIMetaHabilidade.objects.filter(
            pdi__neurodivergente_id=aluno_id,
            pdi__data_criacao__range=(data_inicio, data_fim)
        ).select_related('pdi').order_by('pdi__data_criacao')

        dados_monitoramento = []
        for meta in metas_habilidades:
            dados_monitoramento.append({
                'data': meta.pdi.data_criacao.strftime('%Y-%m-%d'),
                'progresso': meta.progresso
            })

        return JsonResponse({
            'frequencia': {
                'labels': [p['mes'].strftime('%b/%Y') for p in pdis_concluidos],
                'dados': [p['total'] for p in pdis_concluidos],
                'media': round(media_atendimentos, 2)
            },
            'monitoramento': dados_monitoramento
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
