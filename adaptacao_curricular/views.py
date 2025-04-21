from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from .models import AdaptacaoCurricularIndividualizada, BNCCDisciplina, AdaptacaoHabilidade
from datetime import datetime, timedelta
from neurodivergentes.models import Neurodivergente
from configuracoes.models import ConfiguracaoCliente
import os
import logging

logger = logging.getLogger(__name__)

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
        'STATIC_URL': settings.STATIC_URL,
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
    
    # Define o nome do arquivo para download
    filename = f"adaptacao_{adaptacao.aluno.primeiro_nome}_{disciplina.nome}_{timezone.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    return response

@login_required
def imprimir_adaptacao_habilidade(request, adaptacao_habilidade_id):
    """
    Gera um relatório PDF para uma adaptação de habilidade específica.
    """
    # Busca a adaptação de habilidade
    adaptacao_habilidade = get_object_or_404(
        AdaptacaoHabilidade.objects.select_related(
            'aci',
            'aci__aluno',
            'aci__escola',
            'aci__profissional_responsavel',
            'habilidade',
            'habilidade__disciplina'
        ),
        id=adaptacao_habilidade_id
    )
    
    # Prepara o contexto com todos os dados necessários
    context = {
        'adaptacao': adaptacao_habilidade.aci,
        'adaptacao_habilidade': adaptacao_habilidade,
        'data_geracao': timezone.localtime(),
        'STATIC_URL': settings.STATIC_URL,
    }
    
    # Renderiza o template HTML
    html_string = render_to_string('admin/adaptacao_curricular/relatorio_habilidade.html', context)
    
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
    
    # Define o nome do arquivo para download
    filename = f"adaptacao_habilidade_{adaptacao_habilidade.habilidade.codigo}_{timezone.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@login_required
def imprimir_adaptacao_completa(request, adaptacao_id):
    """
    Gera um relatório PDF completo para uma Adaptação Curricular Individualizada (PEI).
    Inclui todas as disciplinas e suas respectivas adaptações.
    """
    # Busca a adaptação com todos os relacionamentos necessários
    adaptacao = get_object_or_404(
        AdaptacaoCurricularIndividualizada.objects.select_related(
            'aluno',
            'escola',
            'profissional_responsavel',
            'profissional_responsavel__user'  # Adicionando o relacionamento com o usuário do profissional
        ),
        id=adaptacao_id
    )
    
    # Busca todas as adaptações de habilidade agrupadas por disciplina
    adaptacoes_por_disciplina = {}
    adaptacoes = AdaptacaoHabilidade.objects.filter(
        aci=adaptacao
    ).select_related(
        'habilidade',
        'habilidade__disciplina'
    ).order_by(
        'habilidade__disciplina__nome',
        'habilidade__codigo'
    )
    
    for adaptacao_habilidade in adaptacoes:
        disciplina = adaptacao_habilidade.habilidade.disciplina
        if disciplina not in adaptacoes_por_disciplina:
            adaptacoes_por_disciplina[disciplina] = []
        adaptacoes_por_disciplina[disciplina].append(adaptacao_habilidade)
    
    # Buscar dados institucionais para o cabeçalho
    config = ConfiguracaoCliente.objects.order_by('-id').first()
    logo_prefeitura_url = request.build_absolute_uri(config.logomarca.url) if config and config.logomarca else None
    nome_prefeitura = config.nome_municipio if config else None
    cnpj_prefeitura = config.cnpj if config else None
    
    # Renderiza o template HTML
    html_string = render_to_string(
        'admin/adaptacao_curricular/relatorio_completo.html',
        {
            'adaptacao': adaptacao,
            'adaptacoes_por_disciplina': adaptacoes_por_disciplina,
            'data_geracao': timezone.now(),
            'logo_prefeitura_url': logo_prefeitura_url,
            'nome_prefeitura': nome_prefeitura,
            'cnpj_prefeitura': cnpj_prefeitura,
        }
    )
    
    # Configura o nome do arquivo
    filename = f"PEI_{adaptacao.aluno.primeiro_nome}_{adaptacao.aluno.ultimo_nome}.pdf"
    
    # Gera o PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    
    # Configurações específicas para o WeasyPrint
    css = CSS(string='''
        @page {
            size: A4;
            margin: 1cm;
            @bottom-center {
                content: none;
            }
        }
        .disciplina-card {
            page-break-before: always;
            break-before: always;
        }
        .disciplina-card:first-of-type {
            page-break-before: avoid;
            break-before: avoid;
        }
        .assinatura {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            page-break-before: auto;
            break-before: auto;
            margin-top: 40px;
            margin-bottom: 40px;
        }
        .footer {
            position: relative;
            margin-top: 20px;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            page-break-before: avoid !important;
            break-before: avoid !important;
        }
    ''')
    
    pdf = html.write_pdf(stylesheets=[css])
    
    # Retorna o PDF como resposta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{filename}"'
    return response

@login_required
def gerar_relatorio_geral_pei(request, aluno_id):
    """
    Gera um relatório geral em HTML para todas as adaptações curriculares de um aluno
    em um período específico.
    """
    try:
        # Obtém as datas do filtro
        data_inicial = request.GET.get('data_inicial')
        data_final = request.GET.get('data_final')
        
        if not data_inicial or not data_final:
            return HttpResponse("Datas não fornecidas", status=400)
        
        # Converte as datas para objetos date
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
        
        # Adiciona um dia à data final para incluir todo o último dia
        data_final_consulta = data_final + timedelta(days=1)
        
        # Busca o aluno
        aluno = get_object_or_404(Neurodivergente, id=aluno_id)
        
        # Busca todas as adaptações do aluno no período
        adaptacoes = AdaptacaoCurricularIndividualizada.objects.filter(
            aluno_id=aluno_id,
            data_cadastro__gte=data_inicial,
            data_cadastro__lt=data_final_consulta
        ).select_related(
            'escola',
            'profissional_responsavel',
            'profissional_responsavel__user'
        ).order_by('data_cadastro')
        
        # Busca todas as adaptações de habilidade para as adaptações encontradas
        adaptacoes_ids = adaptacoes.values_list('id', flat=True)
        adaptacoes_habilidade = AdaptacaoHabilidade.objects.filter(
            aci_id__in=adaptacoes_ids
        ).select_related(
            'habilidade',
            'habilidade__disciplina'
        )
        
        # Agrupa as adaptações de habilidade por adaptação e disciplina
        adaptacoes_por_pei = {}
        for adaptacao in adaptacoes:
            adaptacoes_por_pei[adaptacao.id] = {
                'adaptacao': adaptacao,
                'disciplinas': {}
            }
        
        for adaptacao_habilidade in adaptacoes_habilidade:
            disciplina = adaptacao_habilidade.habilidade.disciplina
            aci_id = adaptacao_habilidade.aci_id
            
            if disciplina.id not in adaptacoes_por_pei[aci_id]['disciplinas']:
                adaptacoes_por_pei[aci_id]['disciplinas'][disciplina.id] = {
                    'disciplina': disciplina,
                    'habilidades': []
                }
            
            adaptacoes_por_pei[aci_id]['disciplinas'][disciplina.id]['habilidades'].append(adaptacao_habilidade)
        
        # Buscar dados institucionais para o cabeçalho
        config = ConfiguracaoCliente.objects.order_by('-id').first()
        logo_prefeitura_url = request.build_absolute_uri(config.logomarca.url) if config and config.logomarca else None
        nome_prefeitura = config.nome_municipio if config else None
        cnpj_prefeitura = config.cnpj if config else None
        
        # Prepara o contexto para o template
        context = {
            'aluno': aluno,
            'data_inicial': data_inicial,
            'data_final': data_final,
            'adaptacoes_por_pei': adaptacoes_por_pei,
            'data_geracao': timezone.now(),
            'logo_prefeitura_url': logo_prefeitura_url,
            'nome_prefeitura': nome_prefeitura,
            'cnpj_prefeitura': cnpj_prefeitura,
        }
        
        # Renderiza o template HTML
        return render(request, 'admin/adaptacao_curricular/relatorio_geral.html', context)
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatório geral: {str(e)}")
        return HttpResponse(f"Erro ao gerar relatório geral: {str(e)}", status=500)
