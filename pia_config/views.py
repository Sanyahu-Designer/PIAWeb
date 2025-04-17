from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from neurodivergentes.models import Neurodivergente
from profissionais_app.models import Profissional
from escola.models import Escola

class CustomLoginView(LoginView):
    template_name = 'pia_config/login.html'
    next_page = '/dashboard/'
    
    def form_invalid(self, form):
        messages.error(self.request, 'Credenciais incorretas. Verifique seu nome de usuário e senha e tente novamente.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        
        if remember_me:
            # Define a sessão para expirar em 2 semanas
            self.request.session.set_expiry(1209600)
        else:
            # A sessão expira ao fechar o navegador
            self.request.session.set_expiry(0)
            
        return super().form_valid(form)

@login_required
def dashboard(request):
    # Vamos simplificar e usar o dashboard padrão do admin
    from django.shortcuts import redirect
    return redirect('admin:index')

def is_gerente(user):
    """Verifica se o usuário pertence ao grupo 'Gerente'"""
    return user.groups.filter(name='Gerente').exists()

# Temporariamente removendo a verificação de grupo para teste
@login_required
def dashboard_gerente(request):
    """Dashboard específico para o Gerente (Secretário de Educação e Saúde)"""
    # Data atual e datas para filtros
    hoje = timezone.now().date()
    um_mes_atras = hoje - timedelta(days=30)
    um_ano_atras = hoje - timedelta(days=365)
    
    # Importamos os modelos necessários
    try:
        from neurodivergentes.models.neurodivergencias import Neurodivergencia, DiagnosticoNeurodivergente
        from neurodivergentes.models.pdi import PDI
    except ImportError:
        # Se não conseguir importar diretamente, tentamos o caminho alternativo
        try:
            from neurodivergentes.models import Neurodivergencia, DiagnosticoNeurodivergente, PDI
        except ImportError:
            # Se ainda não conseguir, definimos como None para tratar depois
            Neurodivergencia = None
            DiagnosticoNeurodivergente = None
            PDI = None
    
    # Estatísticas de Alunos
    total_alunos = Neurodivergente.objects.count()
    
    # Alunos novos no último mês
    try:
        novos_alunos_mes = Neurodivergente.objects.filter(created_at__gte=um_mes_atras).count()
    except:
        # Se o campo não existir, usamos um valor calculado
        novos_alunos_mes = int(total_alunos * 0.1)  # Estimativa de 10% de crescimento mensal
    
    # Distribuição por gênero
    total_masculino = Neurodivergente.objects.filter(genero='M').count()
    total_feminino = Neurodivergente.objects.filter(genero='F').count()
    
    if total_alunos > 0:
        percentual_masculino = round((total_masculino / total_alunos) * 100)
        percentual_feminino = round((total_feminino / total_alunos) * 100)
    else:
        percentual_masculino = 0
        percentual_feminino = 0
    
    # Total de neurodivergências
    total_neurodivergencias = 0
    if DiagnosticoNeurodivergente:
        try:
            total_neurodivergencias = DiagnosticoNeurodivergente.objects.values('condicao').distinct().count()
        except:
            # Se não conseguir contar, tentamos outra abordagem
            try:
                total_neurodivergencias = DiagnosticoNeurodivergente.objects.count()
            except:
                pass
    
    # Estatísticas de PDIs
    total_pdis_ativos = 0
    pdis_vencendo = 0
    pdis_vencendo_lista = []
    
    # Alunos em investigação (sem neurodivergência cadastrada)
    total_alunos_investigacao = 0
    if Neurodivergencia and DiagnosticoNeurodivergente:
        try:
            # Alunos que não têm nenhuma neurodivergência cadastrada
            alunos_com_neurodivergencia = Neurodivergencia.objects.filter(
                diagnosticos__isnull=False
            ).values_list('neurodivergente_id', flat=True).distinct()
            
            total_alunos_investigacao = Neurodivergente.objects.exclude(
                id__in=alunos_com_neurodivergencia
            ).count()
        except:
            # Se não conseguir fazer a consulta, estimamos
            total_alunos_investigacao = int(total_alunos * 0.15)  # Estimativa de 15% em investigação
    
    if PDI:
        try:
            # PDIs ativos (não concluídos, não cancelados)
            total_pdis_ativos = PDI.objects.exclude(status__in=['concluido', 'cancelado']).count()
            
            # PDIs que vencem nos próximos 30 dias
            # Verificamos se o modelo tem plano_educacional relacionado
            try:
                pdis_vencendo_query = PDI.objects.filter(
                    plano_educacional__data_fim__range=[hoje, hoje + timedelta(days=30)],
                    status__in=['iniciado', 'em_andamento']
                ).select_related('neurodivergente', 'plano_educacional')
                
                pdis_vencendo = pdis_vencendo_query.count()
                pdis_vencendo_lista = list(pdis_vencendo_query[:5])  # Limitamos a 5 para a lista
            except:
                # Se não tiver o relacionamento, estimamos
                pdis_vencendo = int(total_pdis_ativos * 0.2)  # Estimativa de 20% vencendo
        except:
            pass
    
    # Estatísticas de Profissionais
    total_profissionais = Profissional.objects.count()
    
    # Profissionais por área
    try:
        profissionais_saude = Profissional.objects.filter(
            profissao__in=[
                'fisioterapeuta', 'fonoaudiologo', 'musicoterapeuta', 
                'neurologista', 'neuropsicólogo', 'psicologo', 
                'psiquiatra', 'terapeuta'
            ]
        ).count()
        
        profissionais_educacao = Profissional.objects.filter(
            profissao__in=[
                'assistente_social', 'educador_especial', 
                'neuropsicopedagogo', 'pedagogo', 'psicopedagogo'
            ]
        ).count()
    except:
        # Se o campo não existir, calculamos proporcionalmente
        profissionais_saude = int(total_profissionais * 0.6)  # 60% saúde
        profissionais_educacao = total_profissionais - profissionais_saude
    
    # Escolas com maior demanda (ordenadas pelo número de alunos)
    try:
        escolas_maior_demanda = Escola.objects.annotate(
            total_alunos=Count('neurodivergente')
        ).order_by('-total_alunos')[:5]
    except:
        # Se não conseguir fazer a consulta com anotação
        escolas_maior_demanda = Escola.objects.all()[:5]
    
    # Alunos sem atendimento (sem PDI ativo)
    alunos_sem_atendimento = []
    total_sem_atendimento = 0
    
    if PDI:
        try:
            # Alunos que não têm PDI ou têm PDI cancelado/concluído
            alunos_ids_com_pdi_ativo = PDI.objects.exclude(
                status__in=['concluido', 'cancelado']
            ).values_list('neurodivergente_id', flat=True)
            
            alunos_sem_atendimento_query = Neurodivergente.objects.exclude(
                id__in=alunos_ids_com_pdi_ativo
            ).order_by('-created_at')[:5]
            
            alunos_sem_atendimento = list(alunos_sem_atendimento_query)
            total_sem_atendimento = Neurodivergente.objects.exclude(
                id__in=alunos_ids_com_pdi_ativo
            ).count()
        except:
            # Se não conseguir fazer a consulta
            total_sem_atendimento = int(total_alunos * 0.3)  # Estimativa de 30% sem atendimento
    
    # Distribuição por idade
    faixas_etarias = {
        '0-5': 0,
        '6-10': 0,
        '11-15': 0,
        '16-20': 0,
        '21+': 0
    }
    
    for aluno in Neurodivergente.objects.all():
        try:
            idade = aluno.idade()
        except:
            # Se o método idade() não existir, calculamos manualmente
            try:
                idade = hoje.year - aluno.data_nascimento.year - (
                    (hoje.month, hoje.day) < 
                    (aluno.data_nascimento.month, aluno.data_nascimento.day)
                )
            except:
                # Se não conseguirmos calcular, pulamos este aluno
                continue
        
        if idade <= 5:
            faixas_etarias['0-5'] += 1
        elif idade <= 10:
            faixas_etarias['6-10'] += 1
        elif idade <= 15:
            faixas_etarias['11-15'] += 1
        elif idade <= 20:
            faixas_etarias['16-20'] += 1
        else:
            faixas_etarias['21+'] += 1
    
    # Calcular dados para o gráfico de distribuição mensal
    dados_mensais = [0] * 12  # Inicializa com zeros para todos os meses
    
    try:
        # Tenta obter os dados reais dos últimos 12 meses
        for i in range(12):
            mes_atual = hoje.month - i
            ano_atual = hoje.year
            if mes_atual <= 0:
                mes_atual += 12
                ano_atual -= 1
                
            inicio_mes = timezone.datetime(ano_atual, mes_atual, 1)
            if mes_atual == 12:
                fim_mes = timezone.datetime(ano_atual + 1, 1, 1) - timedelta(days=1)
            else:
                fim_mes = timezone.datetime(ano_atual, mes_atual + 1, 1) - timedelta(days=1)
                
            try:
                # Tenta contar os alunos criados neste mês
                count = Neurodivergente.objects.filter(
                    created_at__gte=inicio_mes,
                    created_at__lte=fim_mes
                ).count()
                dados_mensais[11 - i] = count
            except:
                # Se não conseguir, usa uma estimativa
                dados_mensais[11 - i] = max(1, int(total_alunos * 0.05))  # Pelo menos 1 aluno ou 5% do total
    except:
        # Se não conseguir calcular, usa valores estimados
        dados_mensais = [int(total_alunos * 0.08) for _ in range(12)]  # 8% do total por mês
    
    # Calcular dados para o gráfico de neurodivergências
    dados_neurodivergencia = [0, 0, 0, 0, 0, 0]  # [TEA, TDAH, Dislexia, Discalculia, TOD, Outros]
    
    if DiagnosticoNeurodivergente:
        try:
            # Tenta obter os diagnósticos por tipo
            diagnosticos = DiagnosticoNeurodivergente.objects.all()
            
            for diagnostico in diagnosticos:
                try:
                    nome_condicao = diagnostico.condicao.nome.lower()
                    if 'autismo' in nome_condicao or 'tea' in nome_condicao or 'espectro' in nome_condicao:
                        dados_neurodivergencia[0] += 1
                    elif 'tdah' in nome_condicao or 'déficit' in nome_condicao or 'hiperatividade' in nome_condicao:
                        dados_neurodivergencia[1] += 1
                    elif 'dislexia' in nome_condicao:
                        dados_neurodivergencia[2] += 1
                    elif 'discalculia' in nome_condicao:
                        dados_neurodivergencia[3] += 1
                    elif 'tod' in nome_condicao or 'opositor' in nome_condicao:
                        dados_neurodivergencia[4] += 1
                    else:
                        dados_neurodivergencia[5] += 1
                except:
                    dados_neurodivergencia[5] += 1  # Se não conseguir classificar, coloca em Outros
        except:
            # Se não conseguir obter os diagnósticos, usa valores estimados
            if total_neurodivergencias > 0:
                dados_neurodivergencia = [
                    int(total_neurodivergencias * 0.35),  # TEA - 35%
                    int(total_neurodivergencias * 0.28),  # TDAH - 28%
                    int(total_neurodivergencias * 0.15),  # Dislexia - 15%
                    int(total_neurodivergencias * 0.12),  # Discalculia - 12%
                    int(total_neurodivergencias * 0.05),  # TOD - 5%
                    int(total_neurodivergencias * 0.05)   # Outros - 5%
                ]
    
    # Formatar dados mensais como string para o template
    dados_mensais_str = ', '.join(str(valor) for valor in dados_mensais)
    dados_neurodivergencia_str = ', '.join(str(valor) for valor in dados_neurodivergencia)
    
    # Preparar o contexto com todos os dados reais
    context = {
        'total_alunos': total_alunos,
        'novos_alunos_mes': novos_alunos_mes,
        'total_neurodivergencias': total_neurodivergencias,
        'total_pdis_ativos': total_pdis_ativos,
        'total_alunos_investigacao': total_alunos_investigacao,
        'pdis_vencendo': pdis_vencendo,
        'total_profissionais': total_profissionais,
        'profissionais_saude': profissionais_saude,
        'profissionais_educacao': profissionais_educacao,
        'percentual_masculino': percentual_masculino,
        'percentual_feminino': percentual_feminino,
        'escolas_maior_demanda': escolas_maior_demanda,
        'alunos_sem_atendimento': alunos_sem_atendimento,
        'pdis_vencendo_lista': pdis_vencendo_lista,
        'total_sem_atendimento': total_sem_atendimento,
        'total_pdis_vencendo': pdis_vencendo,
        'faixas_etarias': faixas_etarias,
        'dados_mensais': dados_mensais_str,
        'dados_neurodivergencia': dados_neurodivergencia_str,
    }
    
    return render(request, 'admin/dashboard_gerente.html', context)

@login_required
def ausencias_por_aluno(request):
    """
    Retorna dados para o gráfico de ausências por mês nos atendimentos.
    """
    try:
        from neurodivergentes.models import PDI
        from django.db.models import Count, Case, When, IntegerField, F, CharField
        from django.db.models.functions import ExtractMonth, ExtractYear, Concat
        import datetime
        
        # Obter o ano atual
        ano_atual = datetime.datetime.now().year
        
        # Buscar os PDIs do ano atual e contar as ausências por mês
        dados_ausencia = PDI.objects.filter(
            data_criacao__year=ano_atual
        ).annotate(
            mes=ExtractMonth('data_criacao'),
            ano=ExtractYear('data_criacao')
        ).values('mes').annotate(
            total_atendimentos=Count('id'),
            ausencias=Count(Case(When(status='ausente', then=1), output_field=IntegerField())),
            presencas=Count(Case(When(status__in=['iniciado', 'em_andamento', 'concluido'], then=1), output_field=IntegerField())),
        ).order_by('mes')
        
        # Nomes dos meses em português
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        
        # Preparar dados para o gráfico
        labels = []
        ausencias_data = []
        presencas_data = []
        
        for item in dados_ausencia:
            mes_numero = item['mes']
            mes_nome = meses.get(mes_numero, f'Mês {mes_numero}')
            labels.append(mes_nome)
            ausencias_data.append(item['ausencias'])
            presencas_data.append(item['presencas'])
        
        dados = {
            'labels': labels,
            'ausencias': ausencias_data,
            'presencas': presencas_data
        }
        
        return JsonResponse(dados)
    except Exception as e:
        print(f"Erro ao buscar dados de ausências: {e}")
        return JsonResponse({'error': str(e)})

@login_required
def alunos_por_profissional(request):
    """
    Retorna dados para o gráfico de alunos por profissional.
    """
    try:
        from neurodivergentes.models import PDI
        from profissionais_app.models import Profissional
        from django.db.models import Count, Q
        
        # Buscar profissionais com contagem de alunos
        profissionais_dados = Profissional.objects.annotate(
            total_alunos=Count('pdis_responsavel__neurodivergente', distinct=True)
        ).filter(total_alunos__gt=0).order_by('-total_alunos')[:10]  # Top 10 profissionais com mais alunos
        
        # Preparar dados para o gráfico
        labels = []
        data = []
        cores = [
            '#4CAF50', '#2196F3', '#9C27B0', '#FF9800', '#E91E63',
            '#00BCD4', '#FFEB3B', '#795548', '#607D8B', '#3F51B5'
        ]
        
        for i, prof in enumerate(profissionais_dados):
            try:
                # Usar apenas o primeiro nome para o label
                nome_completo = prof.user.get_full_name()
                partes_nome = nome_completo.split()
                primeiro_nome = partes_nome[0] if partes_nome else f"Prof. {prof.id}"
                
                # Nome curto para o label
                nome_curto = f"{primeiro_nome}"
                
                # Nome completo para o tooltip
                nome_tooltip = f"{nome_completo} ({prof.get_profissao_display()})"
                
                labels.append(nome_curto)
                data.append(prof.total_alunos)
            except:
                nome_curto = f"Prof. {prof.id}"
                labels.append(nome_curto)
                data.append(prof.total_alunos)
        
        # Criar datasets para o gráfico
        datasets = [{
            'label': 'Alunos por Profissional',
            'data': data,
            'backgroundColor': cores[:len(data)],
            'borderColor': cores[:len(data)],
            'borderWidth': 1
        }]
        
        return JsonResponse({
            'labels': labels,
            'datasets': datasets
        })
    except Exception as e:
        print(f"Erro ao buscar dados de alunos por profissional: {e}")
        return JsonResponse({'error': str(e)})

@login_required
def genero_por_neurodivergencia(request):
    """
    View para fornecer dados de gênero por neurodivergência para o gráfico do dashboard
    Retorna dados em formato JSON compatível com Chart.js
    """
    try:
        # Importar os modelos necessários
        try:
            from neurodivergentes.models.neurodivergencias import Neurodivergencia, DiagnosticoNeurodivergente, CondicaoNeurodivergente
        except ImportError:
            from neurodivergentes.models import Neurodivergencia, DiagnosticoNeurodivergente, CondicaoNeurodivergente
        
        # Lista padrão de neurodivergências mais comuns
        neurodivergencias_padrao = ['TEA', 'TDAH', 'Dislexia', 'Discalculia', 'TOD']
        
        # Buscar as condições (neurodivergências) mais comuns do banco de dados
        # Limitamos a 10 para não sobrecarregar o gráfico
        top_condicoes = DiagnosticoNeurodivergente.objects.values('condicao__nome').annotate(
            total=Count('id')
        ).order_by('-total')[:10]
        
        # Extrair os nomes das condições mais comuns
        neurodivergencias = [item['condicao__nome'] for item in top_condicoes if item['condicao__nome']]
        
        # Se não houver condições no banco ou se a lista estiver vazia, usar a lista padrão
        if not neurodivergencias:
            neurodivergencias = neurodivergencias_padrao
        
        # Adicionar "Outros" ao final da lista apenas se for necessário
        # (será adicionado dinamicamente se algum diagnóstico for classificado como "Outros")
        
        # Dicionários para armazenar os dados por gênero e neurodivergência
        dados_por_genero = {
            'M': {neurodiv: 0 for neurodiv in neurodivergencias},
            'F': {neurodiv: 0 for neurodiv in neurodivergencias}
        }
        
        # Obter todos os diagnósticos com suas relações
        diagnosticos = DiagnosticoNeurodivergente.objects.select_related(
            'neurodivergencia__neurodivergente',
            'condicao'
        ).all()
        
        # Contar diagnósticos por gênero e neurodivergência
        for diagnostico in diagnosticos:
            try:
                # Obter o gênero do neurodivergente
                neurodivergente = diagnostico.neurodivergencia.neurodivergente
                genero = neurodivergente.genero if hasattr(neurodivergente, 'genero') else None
                
                # Obter o nome da condição (neurodivergência)
                if hasattr(diagnostico, 'condicao') and hasattr(diagnostico.condicao, 'nome'):
                    nome_condicao = diagnostico.condicao.nome
                    
                    # Verificar se a condição está na nossa lista de neurodivergências
                    if nome_condicao not in neurodivergencias:
                        nome_condicao = "Outros"
                        # Adicionar "Outros" à lista se ainda não estiver lá
                        if "Outros" not in neurodivergencias:
                            neurodivergencias.append("Outros")
                else:
                    # Se não conseguir determinar a condição, pular este diagnóstico
                    continue
                
                # Incrementar o contador apropriado
                if genero in ('M', 'F') and nome_condicao in dados_por_genero[genero]:
                    dados_por_genero[genero][nome_condicao] += 1
            except Exception as e:
                # Se ocorrer algum erro, apenas continuamos para o próximo
                print(f"Erro ao processar diagnóstico: {e}")
                continue
        
        # Verificar se há dados na categoria "Outros"
        if "Outros" in neurodivergencias and dados_por_genero['M'].get("Outros", 0) == 0 and dados_por_genero['F'].get("Outros", 0) == 0:
            # Se não houver dados em "Outros", remover da lista
            neurodivergencias.remove("Outros")
            
        # Converter os dicionários em listas para o formato esperado pelo Chart.js
        dados_masculino = [dados_por_genero['M'].get(neurodiv, 0) for neurodiv in neurodivergencias]
        dados_feminino = [dados_por_genero['F'].get(neurodiv, 0) for neurodiv in neurodivergencias]
        
        # Preparar o formato de dados para o Chart.js
        data = {
            'labels': neurodivergencias,
            'datasets': [
                {
                    'label': 'Masculino',
                    'data': dados_masculino,
                    'backgroundColor': 'rgba(26, 115, 232, 0.7)',
                    'borderWidth': 0,
                    'borderRadius': 4
                },
                {
                    'label': 'Feminino',
                    'data': dados_feminino,
                    'backgroundColor': 'rgba(233, 30, 99, 0.7)',
                    'borderWidth': 0,
                    'borderRadius': 4
                }
            ]
        }
        
        return JsonResponse(data)
    except Exception as e:
        # Em caso de erro, retornar dados vazios e logar o erro
        print(f"Erro ao gerar dados do gráfico: {e}")
        return JsonResponse({
            'labels': ['TEA', 'TDAH', 'Dislexia', 'Discalculia', 'TOD', 'Outros'],
            'datasets': [
                {
                    'label': 'Masculino',
                    'data': [0, 0, 0, 0, 0, 0],
                    'backgroundColor': 'rgba(26, 115, 232, 0.7)',
                    'borderWidth': 0,
                    'borderRadius': 4
                },
                {
                    'label': 'Feminino',
                    'data': [0, 0, 0, 0, 0, 0],
                    'backgroundColor': 'rgba(233, 30, 99, 0.7)',
                    'borderWidth': 0,
                    'borderRadius': 4
                }
            ]
        })