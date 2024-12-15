from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_GET
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
from django.conf import settings
import os
from .models import (
    Neurodivergente, PDI, PlanoEducacional, RegistroEvolucao,
    Monitoramento, Frequencia, ParecerAvaliativo, CondicaoNeurodivergente
)

def calculate_progresso_total(pdi):
    """Calcula o progresso total do PDI"""
    metas = pdi.metas_habilidades.all()
    if not metas:
        return 0
    return int(sum(meta.progresso for meta in metas) / len(metas))

@login_required
def pdi_popup_view(request, pdi_id):
    pdi = get_object_or_404(
        PDI.objects.select_related(
            'neurodivergente',
            'pedagogo_responsavel'
        ).prefetch_related(
            'metas_habilidades__meta_habilidade'
        ),
        id=pdi_id
    )
    
    # Calcula o progresso usando a função auxiliar
    progresso = calculate_progresso_total(pdi)
    
    context = {
        'pdi': pdi,
        'progresso': progresso,
    }
    
    return render(request, 'admin/neurodivergentes/pdi/popup_view.html', context)

@login_required
def imprimir_pdi(request, pdi_id):
    # Busca o PDI com todos os relacionamentos necessários
    pdi = get_object_or_404(PDI.objects.select_related(
        'neurodivergente',
        'pedagogo_responsavel'
    ).prefetch_related(
        'metas_habilidades__meta_habilidade'
    ), id=pdi_id)
    
    # Prepara o contexto com todos os dados necessários
    context = {
        'pdi': pdi,
        'data_impressao': timezone.now(),
        'metas': pdi.metas_habilidades.all().select_related('meta_habilidade'),
        'progresso_total': calculate_progresso_total(pdi)
    }
    
    # Configura as fontes
    font_config = FontConfiguration()
    css_string = """
        @font-face {
            font-family: 'Roboto';
            src: url('%s') format('truetype');
            font-weight: normal;
        }
        @font-face {
            font-family: 'Roboto';
            src: url('%s') format('truetype');
            font-weight: bold;
        }
    """ % (
        os.path.join(settings.STATIC_ROOT, 'fonts/Roboto-Regular.ttf'),
        os.path.join(settings.STATIC_ROOT, 'fonts/Roboto-Bold.ttf')
    )
    
    # Renderiza o template HTML
    html_string = render_to_string('neurodivergentes/pdi_print.html', context)
    
    # Cria o PDF com as configurações de fonte
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    css = CSS(string=css_string, font_config=font_config)
    pdf = html.write_pdf(
        stylesheets=[css],
        font_config=font_config,
        presentational_hints=True
    )
    
    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=pdi_{pdi.id}.pdf'
    
    return response

@login_required
def imprimir_pdis_aluno(request, aluno_id):
    neurodivergente = get_object_or_404(Neurodivergente, id=aluno_id)
    
    # Filtros de data
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    pdis = PDI.objects.filter(neurodivergente=neurodivergente)
    
    if date_from:
        pdis = pdis.filter(data_criacao__gte=datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        pdis = pdis.filter(data_criacao__lte=datetime.strptime(date_to, '%Y-%m-%d'))
    
    context = {
        'neurodivergente': neurodivergente,
        'pdis': pdis,
        'data_impressao': timezone.now()
    }
    
    html_string = render_to_string('neurodivergentes/relatorio_pdis.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=pdis_{neurodivergente.id}.pdf'
    
    return response

@login_required
def gerar_relatorio_pdf(request, neurodivergente_id):
    neurodivergente = get_object_or_404(Neurodivergente, id=neurodivergente_id)
    
    context = {
        'neurodivergente': neurodivergente,
        'pdis': PDI.objects.filter(neurodivergente=neurodivergente),
        'evolucoes': RegistroEvolucao.objects.filter(neurodivergente=neurodivergente),
        'monitoramentos': Monitoramento.objects.filter(neurodivergente=neurodivergente),
        'frequencias': Frequencia.objects.filter(neurodivergente=neurodivergente),
        'pareceres': ParecerAvaliativo.objects.filter(neurodivergente=neurodivergente),
        'data_geracao': timezone.now()
    }
    
    html_string = render_to_string('neurodivergentes/relatorio.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=relatorio_{neurodivergente.id}.pdf'
    
    return response

@login_required
def grafico_evolucao(request, neurodivergente_id):
    neurodivergente = get_object_or_404(Neurodivergente, id=neurodivergente_id)
    
    # Dados para o gráfico de dispersão (evolução)
    monitoramentos = Monitoramento.objects.filter(
        neurodivergente=neurodivergente
    ).order_by('data')
    
    datas = [m.data for m in monitoramentos]
    niveis = [m.nivel for m in monitoramentos]
    metas = [m.meta for m in monitoramentos]
    
    # Dados para o gráfico de barras (frequência)
    frequencias = Frequencia.objects.filter(
        neurodivergente=neurodivergente,
        ano=timezone.now().year
    ).order_by('mes')
    
    meses = [f.get_mes_display() for f in frequencias]
    atendimentos = [f.total_atendimentos for f in frequencias]
    
    # Criar subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            'Evolução do Desenvolvimento',
            'Frequência de Atendimentos'
        )
    )
    
    # Adicionar gráfico de dispersão
    fig.add_trace(
        go.Scatter(
            x=datas,
            y=niveis,
            mode='lines+markers',
            name='Nível de Desenvolvimento',
            text=metas,
            hovertemplate='%{text}<br>Nível: %{y}%<br>Data: %{x}'
        ),
        row=1, col=1
    )
    
    # Adicionar gráfico de barras
    fig.add_trace(
        go.Bar(
            x=meses,
            y=atendimentos,
            name='Atendimentos',
            hovertemplate='Mês: %{x}<br>Atendimentos: %{y}'
        ),
        row=2, col=1
    )
    
    # Atualizar layout
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text=f'Evolução de {neurodivergente}',
        title_x=0.5
    )
    
    # Atualizar eixos
    fig.update_yaxes(title_text='Nível (%)', row=1, col=1)
    fig.update_yaxes(title_text='Quantidade', row=2, col=1)
    
    # Converter para JSON
    grafico_json = fig.to_json()
    
    return JsonResponse({'grafico': grafico_json})

@login_required
@require_GET
def get_condicoes(request):
    """Retorna as condições neurodivergentes de uma categoria específica."""
    categoria_id = request.GET.get('categoria_id')
    if not categoria_id:
        return JsonResponse({'error': 'Categoria não especificada'}, status=400)
    
    try:
        condicoes = CondicaoNeurodivergente.objects.filter(
            categoria_id=categoria_id,
            ativo=True
        ).values('id', 'nome', 'cid_10')
        
        return JsonResponse({
            'condicoes': list(condicoes)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)