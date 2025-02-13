import os
import io
import json
import base64
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder

from .models import PDI, PDIMetaHabilidade

def gerar_dados_frequencia(pdis_concluidos, media_atendimentos):
    """Gera os dados de frequência de atendimentos para Chart.js"""
    try:
        labels = [p['mes'].strftime('%b/%Y') if p['mes'] else '' for p in pdis_concluidos]
        dados = [float(p['total']) if p['total'] is not None else 0 for p in pdis_concluidos]
        media = float(media_atendimentos) if media_atendimentos is not None else 0
        
        return {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Atendimentos',
                    'data': dados,
                    'backgroundColor': 'rgba(0, 123, 255, 0.7)',
                    'borderColor': 'rgba(0, 123, 255, 1)',
                    'borderWidth': 1
                },
                {
                    'label': f'Média: {round(media, 2)}',
                    'data': [media] * len(labels),
                    'type': 'line',
                    'borderColor': 'rgba(220, 53, 69, 1)',
                    'borderDash': [5, 5],
                    'fill': 0
                }
            ]
        }
    except Exception as e:
        print(f"Erro em gerar_dados_frequencia: {str(e)}")
        return {
            'labels': [],
            'datasets': [
                {'label': 'Atendimentos', 'data': []},
                {'label': 'Média', 'data': []}
            ]
        }

def gerar_dados_monitoramento(dados_monitoramento):
    """Gera os dados de monitoramento do PDI para Chart.js"""
    try:
        # Converte as datas para o formato dd/mm/aaaa
        datas = [datetime.strptime(dado['data'], '%Y-%m-%d').strftime('%d/%m/%Y') for dado in dados_monitoramento]
        progressos = [float(dado['progresso']) if dado['progresso'] is not None else 0 for dado in dados_monitoramento]
        descricoes = [dado['descricao'] for dado in dados_monitoramento]
        
        return {
            'labels': datas,
            'datasets': [{
                'label': 'Progresso',
                'data': progressos,
                'backgroundColor': 'rgba(40, 167, 69, 0.7)',
                'borderColor': 'rgba(40, 167, 69, 1)',
                'borderWidth': 1,
                'pointRadius': 4,
                'pointBackgroundColor': 'rgba(40, 167, 69, 1)',
                'fill': 0
            }],
            'descricoes': descricoes  # Adicionando descrições separadamente
        }
    except Exception as e:
        print(f"Erro em gerar_dados_monitoramento: {str(e)}")
        return {
            'labels': [],
            'datasets': [{
                'label': 'Progresso',
                'data': [],
                'fill': 0
            }]
        }

@require_GET
def dados_graficos_parecer(request):
    """
    Gera os gráficos do parecer avaliativo usando Matplotlib.
    Parâmetros esperados na URL:
    - aluno_id: ID do neurodivergente
    - data_inicio: Data inicial no formato YYYY-MM-DD
    - data_fim: Data final no formato YYYY-MM-DD
    """
    try:
        aluno_id = request.GET.get('aluno_id')
        data_inicio_str = request.GET.get('data_inicio')
        data_fim_str = request.GET.get('data_fim')
        
        print(f"Recebido: aluno_id={aluno_id}, data_inicio={data_inicio_str}, data_fim={data_fim_str}")
        
        if not all([aluno_id, data_inicio_str, data_fim_str]):
            return JsonResponse({'error': 'Parâmetros faltando'}, status=400)
            
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        except ValueError as e:
            print(f"Erro ao converter datas: {e}")
            return JsonResponse({'error': 'Formato de data inválido'}, status=400)

        print("\n=== Buscando dados de PDIs concluídos ===")
        query_pdis = PDI.objects.filter(
            neurodivergente_id=aluno_id,
            status='concluido',
            data_criacao__range=(data_inicio, data_fim)
        )
        print(f"Query base PDIs: {str(query_pdis.query)}")
        
        pdis_concluidos = query_pdis.annotate(
            mes=TruncMonth('data_criacao')
        ).values('mes').annotate(
            total=Count('id')
        ).order_by('mes')
        
        print(f"PDIs encontrados: {list(pdis_concluidos)}")

        # Calcula a média de atendimentos
        media_atendimentos = pdis_concluidos.aggregate(
            media=Avg('total')
        )['media'] or 0

        print("\n=== Buscando dados de metas e habilidades ===")
        query_metas = PDIMetaHabilidade.objects.filter(
            pdi__neurodivergente_id=aluno_id,
            pdi__data_criacao__range=(data_inicio, data_fim)
        ).select_related('pdi')
        
        print(f"Query metas: {str(query_metas.query)}")
        metas_habilidades = query_metas.order_by('pdi__data_criacao')
        print(f"Total de metas encontradas: {metas_habilidades.count()}")

        dados_monitoramento = [
            {
                'data': meta.pdi.data_criacao.strftime('%Y-%m-%d'),
                'progresso': meta.progresso,
                'descricao': str(meta.meta_habilidade)
            } for meta in metas_habilidades
        ]

        # Gera os dados dos gráficos
        dados_frequencia = gerar_dados_frequencia(pdis_concluidos, media_atendimentos)
        dados_monitoramento = gerar_dados_monitoramento(dados_monitoramento)

        print("\n=== Preparando resposta ===")
        try:
            # Não precisamos mais converter os valores booleanos pois já estão como números
            response_data = {
                'dados_frequencia': dados_frequencia,
                'dados_monitoramento': dados_monitoramento
            }
            
            # Converte para string para debug
            json_str = json.dumps(response_data, cls=DjangoJSONEncoder, indent=2)
            print("JSON gerado:")
            print(json_str)
            
            return JsonResponse(response_data, encoder=DjangoJSONEncoder, safe=False)
        except Exception as e:
            print(f"Erro ao preparar JSON: {str(e)}")
            return JsonResponse({'error': 'Erro ao preparar dados', 'detalhes': str(e)}, status=400)
    except Exception as e:
        import traceback
        print(f"\n=== ERRO NÃO TRATADO ===")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return JsonResponse({
            'error': 'Erro interno',
            'tipo': type(e).__name__,
            'mensagem': str(e)
        }, status=400)
