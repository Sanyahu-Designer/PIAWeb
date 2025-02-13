from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html
from django.utils.html import format_html
from django.db.models import Count, Subquery, OuterRef, Avg
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template import loader
from .choices import MESES
from escola.models import ModalidadeEnsino, ProgramaEducacional, Recurso, Escola
from escola.forms import EscolaForm
from .models import (
    Neurodivergente, GrupoFamiliar, HistoricoEscolar,
    Neurodivergencia, CondicaoNeurodivergente,
    CategoriaNeurodivergente, DiagnosticoNeurodivergente,
    Anamnese, PDI, MetaHabilidade, PDIMetaHabilidade,
    PlanoEducacional, AdaptacaoCurricular, RegistroEvolucao,
    Monitoramento, ParecerAvaliativo
)
from .forms import (
    NeurodivergenteForms, PDIForm, PlanoEducacionalForm,
    AdaptacaoCurricularForm, RegistroEvolucaoForm,
    MonitoramentoForm, ParecerAvaliativoForm
)

from django.db.models import Max
from django.shortcuts import get_object_or_404

class GrupoFamiliarInline(admin.TabularInline):
    model = GrupoFamiliar
    extra = 1
    
    formfield_overrides = {
        models.DateField: {
            'widget': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'vDateField date-input',
                },
                format='%Y-%m-%d'
            )
        }
    }
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        class CustomFormset(formset):
            def _construct_form(self, *args, **kwargs):
                form = super()._construct_form(*args, **kwargs)
                if form.instance and form.instance.data_nascimento:
                    form.initial['data_nascimento'] = form.instance.data_nascimento.strftime('%Y-%m-%d')
                return form
        return CustomFormset

@admin.register(Neurodivergente)
class NeurodivergenteAdmin(admin.ModelAdmin):
    form = NeurodivergenteForms
    inlines = [GrupoFamiliarInline]
    readonly_fields = ['foto_preview']
    list_display = ['primeiro_nome', 'ultimo_nome', 'idade', 'cidade', 'estado']
    list_filter = ['estado', 'genero']
    search_fields = ['primeiro_nome', 'ultimo_nome', 'cpf']
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'})}
    }

    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'primeiro_nome', 'ultimo_nome', 'data_nascimento', 'genero',
                'cpf', 'rg', 'foto_perfil', 'foto_preview'
            ),
            'classes': ('tab-dados-pessoais',)
        }),
      #  ('Localização', {
      #      'fields': (
      #          'estado_nascimento', 'cidade_nascimento'
      #      ),
      #      'classes': ('tab-localizacao',)
      #  }),
        ('Endereço', {
            'fields': (
                'cep', 'endereco', 'numero', 'complemento',
                'bairro', 'cidade', 'estado'
            ),
            'classes': ('tab-endereco',)
        }),
        ('Contato', {
            'fields': (
                'celular', 'email'
            ),
            'classes': ('tab-contato',)
        })
    )


    class Media:
        css = {
            'all': ('admin/css/neurodivergentes_forms.css',)
        }
        js = (
            'admin/js/jquery.mask.min.js',
            'admin/js/neurodivergentes_admin.js',
            'admin/js/grupo_familiar.js',
        )

@admin.register(CategoriaNeurodivergente)
class CategoriaNeurodivergentesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem']
    ordering = ['ordem', 'nome']
    search_fields = ['nome']

@admin.register(CondicaoNeurodivergente)
class CondicaoNeurodivergentesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'cid_10', 'ativo']
    list_filter = ['categoria', 'ativo']
    search_fields = ['nome', 'cid_10']
    ordering = ['categoria', 'nome']

class DiagnosticoInline(admin.TabularInline):
    model = DiagnosticoNeurodivergente
    extra = 1
    min_num = 1
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'})}
    }

class AdaptacaoCurricularInline(admin.StackedInline):
    model = AdaptacaoCurricular
    form = AdaptacaoCurricularForm
    extra = 1
    verbose_name = 'Nova adaptação curricular'
    verbose_name_plural = 'Adaptações Curriculares'

@admin.register(Neurodivergencia)
class NeurodivergenciaAdmin(admin.ModelAdmin):
    inlines = [DiagnosticoInline]
    list_display = ['neurodivergente', 'data_diagnostico', 'profissional_diagnostico']
    list_filter = ['data_diagnostico']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'})}
    }
    
    fieldsets = (
        ('Neurodivergente', {
            'fields': ('neurodivergente',)
        }),
        ('Diagnóstico', {
            'fields': (
                'data_diagnostico',
                'profissional_diagnostico',
                'observacoes',
                'laudo_medico'
            ),
            'classes': ('wide', 'diagnosticos-container')
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/neurodivergentes_forms.css',)
        }
        js = ('admin/js/neurodivergentes_admin.js',)

@admin.register(MetaHabilidade)
class MetaHabilidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']
class PDIMetaHabilidadeInline(admin.TabularInline):
    model = PDIMetaHabilidade
    extra = 1
    min_num = 1
    fields = ('meta_habilidade', 'progresso')
    classes = ('meta-habilidade-inline',)

@admin.register(PDI)
class PDIAdmin(admin.ModelAdmin):
    form = PDIForm
    inlines = [PDIMetaHabilidadeInline]
    list_display = ['get_aluno_nome', 'get_total_pdis', 'get_ultimo_pdi', 'get_view_button']
    list_filter = ['neurodivergente']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']
    list_per_page = 20

    def get_queryset(self, request):
        """
        Retorna apenas o PDI mais recente por aluno na lista inicial,
        ou todos os PDIs se um filtro de aluno estiver ativo.
        """
        self.request = request
        queryset = super().get_queryset(request).select_related(
            'neurodivergente', 'pedagogo_responsavel'
        ).prefetch_related('metas_habilidades')

        neurodivergente_id = request.GET.get('neurodivergente__id__exact')
        if neurodivergente_id:
            # Lista todos os PDIs do aluno filtrado
            return queryset.filter(neurodivergente_id=neurodivergente_id).order_by('-data_criacao')

        # Lista inicial: retorna apenas o PDI mais recente por aluno
        from django.db.models import Max
        latest_pdi_ids = queryset.values('neurodivergente').annotate(
            max_id=Max('id')
        ).values_list('max_id', flat=True)

        return queryset.filter(id__in=latest_pdi_ids).order_by('neurodivergente__primeiro_nome')

    def get_object(self, request, object_id, from_field=None):
        """
        Personaliza a busca de objetos para garantir que qualquer PDI seja carregado,
        independentemente do queryset usado na exibição agrupada.
        """
        queryset = super().get_queryset(request)
        return get_object_or_404(PDI, pk=object_id)

    def get_aluno_nome(self, obj):
        """
        Gera o link correto para o nome do aluno:
        - Lista inicial: redireciona para a lista de PDIs do aluno.
        - Lista filtrada: redireciona para o detalhe do PDI.
        """
        if not obj.neurodivergente:
            return '-'

        if hasattr(self, 'request') and 'neurodivergente__id__exact' not in self.request.GET:
            # Link para a lista de PDIs do aluno
            url = f"{reverse('admin:neurodivergentes_pdi_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
        else:
            # Link para o detalhe do PDI
            url = reverse('admin:neurodivergentes_pdi_change', args=[obj.id])

        nome_completo = f"{obj.neurodivergente.primeiro_nome} {obj.neurodivergente.ultimo_nome}"
        return format_html(
            '<a href="{}" style="color: #447e9b; text-decoration: none;">{}</a>',
            url,
            nome_completo
        )
    get_aluno_nome.short_description = 'Aluno/Paciente'
    get_aluno_nome.admin_order_field = 'neurodivergente__primeiro_nome'

    def get_total_pdis(self, obj):
        """
        Retorna o número total de PDIs associados ao aluno.
        """
        if not obj.neurodivergente:
            return 0
        return PDI.objects.filter(neurodivergente=obj.neurodivergente).count()
    get_total_pdis.short_description = 'Total de PDIs'

    def get_ultimo_pdi(self, obj):
        """
        Retorna a data de criação do último PDI.
        """
        return obj.data_criacao if obj.data_criacao else '-'
    get_ultimo_pdi.short_description = 'Último PDI'

    def changelist_view(self, request, extra_context=None):
        """
        Ajusta as colunas exibidas na listagem com base no contexto:
        - Lista inicial: exibe agrupamento.
        - Lista detalhada: exibe todos os PDIs do aluno.
        """
        self.request = request
        if 'neurodivergente__id__exact' in request.GET:
            self.list_display = ['get_aluno_nome', 'data_criacao', 'get_progresso', 'status', 'get_view_button']
        else:
            self.list_display = ['get_aluno_nome', 'get_total_pdis', 'get_ultimo_pdi', 'get_view_button']
        return super().changelist_view(request, extra_context)

    def get_progresso(self, obj):
        """
        Calcula o progresso médio das metas associadas ao PDI.
        """
        metas = obj.metas_habilidades.all()
        if not metas:
            return '0%'
        total_progresso = sum(meta.progresso for meta in metas)
        media_progresso = total_progresso / len(metas)
        return f'{int(media_progresso)}%'
    get_progresso.short_description = 'Progresso (%)'

    def get_view_button(self, obj):
        """
        Gera um botão de ação para visualizar detalhes do PDI.
        """
        if not obj.id:
            return '-'

        if hasattr(self, 'request') and 'neurodivergente__id__exact' in self.request.GET:
            return format_html(
                '<button type="button" onclick="loadPDIDetails({})" class="view-pdi-btn" '
                'style="background-color: #447e9b; color: white; padding: 5px 10px; '
                'border-radius: 3px; border: none; cursor: pointer;">'
                '<i class="fas fa-eye" style="margin-right: 5px;"></i> Visualizar PDI</button>',
                obj.id
            )
        else:
            url = f"{reverse('admin:neurodivergentes_pdi_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
            return format_html(
                '<a href="{}" class="button" style="background-color: #447e9b; color: white; '
                'padding: 5px 10px; border-radius: 3px; text-decoration: none; display: inline-block;">'
                '<i class="fas fa-eye" style="margin-right: 5px;"></i> Visualizar PDIs</a>',
                url
            )
    get_view_button.short_description = 'Ações'

    class Media:
        """
        Inclui arquivos CSS e JavaScript adicionais para customização.
        """
        css = {
            'all': (
                'admin/css/pdi_forms.css',
                'admin/css/pdi_popup.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            )
        }

        js = (
            'admin/js/pdi_admin.js',
            'admin/js/pdi_popup.js',
        )

    fieldsets = (
        (None, {
            'fields': ('neurodivergente', 'data_criacao', 'status', 'observacoes', 'pedagogo_responsavel')
        }),
    )

    class Meta:
        verbose_name = 'Adaptação Curricular Individualizada'
        verbose_name_plural = 'Adaptações Curriculares Individualizadas'

@admin.register(Monitoramento)
class MonitoramentoAdmin(admin.ModelAdmin):
    form = MonitoramentoForm
    list_display = ['get_aluno_nome', 'get_total_peis', 'get_ultimo_pei', 'get_view_button']
    list_filter = ['neurodivergente']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']
    list_per_page = 20
    
    def changelist_view(self, request, extra_context=None):
        # Adiciona os dados para o modal de relatório
        extra_context = extra_context or {}
        extra_context['meses'] = MESES
        extra_context['anos'] = range(2020, 2051)
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        """Retorna apenas o PEI mais recente por aluno na lista inicial,
        ou todos os PEIs se um filtro de aluno estiver ativo."""
        self.request = request
        queryset = super().get_queryset(request).select_related('neurodivergente')

        neurodivergente_id = request.GET.get('neurodivergente__id__exact')
        if neurodivergente_id:
            # Lista todos os PEIs do aluno filtrado
            return queryset.filter(neurodivergente_id=neurodivergente_id).order_by('-ano', '-mes')

        # Lista inicial: retorna apenas o PEI mais recente por aluno
        latest_pei_ids = queryset.values('neurodivergente').annotate(
            max_id=models.Max('id')
        ).values_list('max_id', flat=True)

        return queryset.filter(id__in=latest_pei_ids).order_by('neurodivergente__primeiro_nome')

    def get_object(self, request, object_id, from_field=None):
        """Personaliza a busca de objetos para garantir que qualquer PEI seja carregado,
        independentemente do queryset usado na exibição agrupada."""
        queryset = super().get_queryset(request)
        return get_object_or_404(Monitoramento, pk=object_id)

    def get_aluno_nome(self, obj):
        """Gera o link correto para o nome do aluno:
        - Lista inicial: redireciona para a lista de PEIs do aluno.
        - Lista filtrada: redireciona para o detalhe do PEI."""
        if not obj.neurodivergente:
            return '-'

        if hasattr(self, 'request') and 'neurodivergente__id__exact' not in self.request.GET:
            # Link para a lista de PEIs do aluno
            url = f"{reverse('admin:neurodivergentes_monitoramento_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
        else:
            # Link para o detalhe do PEI
            url = reverse('admin:neurodivergentes_monitoramento_change', args=[obj.id])

        nome_completo = f"{obj.neurodivergente.primeiro_nome} {obj.neurodivergente.ultimo_nome}"
        return format_html(
            '<a href="{}" style="color: #447e9b; text-decoration: none;">{}</a>',
            url,
            nome_completo
        )
    get_aluno_nome.short_description = 'Aluno/Paciente'
    get_aluno_nome.admin_order_field = 'neurodivergente__primeiro_nome'

    def get_total_peis(self, obj):
        """Retorna o total de PEIs do aluno."""
        if not obj.neurodivergente:
            return '0'
        return Monitoramento.objects.filter(neurodivergente=obj.neurodivergente).count()
    get_total_peis.short_description = 'Total de PEIs'

    def get_ultimo_pei(self, obj):
        """Retorna o mês/ano do último PEI."""
        if not obj.neurodivergente:
            return '-'
        ultimo = Monitoramento.objects.filter(
            neurodivergente=obj.neurodivergente
        ).order_by('-ano', '-mes').first()
        
        if ultimo:
            return f"{ultimo.get_mes_display()}/{ultimo.ano}"
        return '-'
    get_ultimo_pei.short_description = 'Último PEI'

    def get_list_display(self, request):
        """Altera as colunas exibidas dependendo se estamos na lista inicial
        ou na lista de PEIs de um aluno."""
        if request.GET.get('neurodivergente__id__exact'):
            # Na página de PEIs do aluno
            return ['neurodivergente', 'get_mes_ano', 'get_metas', 'get_acoes']
        # Na página inicial
        return ['get_aluno_nome', 'get_total_peis', 'get_ultimo_pei', 'get_view_button']

    def get_mes_ano(self, obj):
        """Retorna o mês/ano formatado."""
        return f"{obj.get_mes_display()}/{obj.ano}"
    get_mes_ano.short_description = 'Mês/Ano'
    get_mes_ano.admin_order_field = 'ano'

    def get_metas(self, obj):
        """Retorna as metas do PEI."""
        return ", ".join([meta.nome for meta in obj.metas.all()])
    get_metas.short_description = 'Metas/Habilidades'

    def get_view_button(self, obj):
        """Retorna o botão de visualização que leva para a lista de PEIs do aluno."""
        if not obj.neurodivergente:
            return ''
        
        url = f"{reverse('admin:neurodivergentes_monitoramento_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
        return format_html(
            '<a class="btn btn-info btn-sm" style="min-width: 100px;" href="{}"><i class="fas fa-eye me-1"></i> Ver PEIs</a>',
            url
        )
    get_view_button.short_description = 'Ver PEIs'

    def get_acoes(self, obj):
        """Retorna os botões de ação para a lista de PEIs do aluno."""
        editar_url = reverse('admin:neurodivergentes_monitoramento_change', args=[obj.id])
        imprimir_url = reverse('neurodivergentes:imprimir_pei', args=[obj.id])
        
        return format_html(
            '<div class="btn-group">' 
            '<a href="{}" class="btn btn-sm btn-info" title="Editar"><i class="fas fa-edit"></i></a>' 
            '<button type="button" class="btn btn-sm btn-primary" onclick="window.open(\'{}\')" title="Imprimir">' 
            '<i class="fas fa-print"></i> Imprimir</button>' 
            '</div>',
            editar_url,
            imprimir_url
        )
    get_acoes.short_description = 'Ações'

    class Media:
        css = {
            'all': (
                'admin/css/pei_forms.css',
                'admin/css/pei_popup.css',
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            )
        }
        js = (
            'admin/js/pei_admin.js',
            'admin/js/pei_popup.js',
        )

@admin.register(RegistroEvolucao)
class RegistroEvolucaoAdmin(admin.ModelAdmin):
    form = RegistroEvolucaoForm
    list_display = ['get_aluno_nome', 'get_total_evolucoes', 'get_ultima_evolucao', 'get_view_button']
    list_filter = ['neurodivergente']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome', 'descricao']
    list_per_page = 20

    def get_queryset(self, request):
        """
        Retorna apenas a evolução mais recente por aluno na lista inicial,
        ou todas as evoluções se um filtro de aluno estiver ativo.
        """
        self.request = request
        queryset = super().get_queryset(request).select_related(
            'neurodivergente', 'profissional'
        )

        neurodivergente_id = request.GET.get('neurodivergente__id__exact')
        if neurodivergente_id:
            # Lista todas as evoluções do aluno filtrado
            return queryset.filter(neurodivergente_id=neurodivergente_id).order_by('-data')

        # Lista inicial: retorna apenas a evolução mais recente por aluno
        from django.db.models import Max
        latest_evolucao_ids = queryset.values('neurodivergente').annotate(
            max_id=Max('id')
        ).values_list('max_id', flat=True)

        return queryset.filter(id__in=latest_evolucao_ids).order_by('neurodivergente__primeiro_nome')

    def get_object(self, request, object_id, from_field=None):
        """
        Personaliza a busca de objetos para garantir que qualquer evolução seja carregada,
        independentemente do queryset usado na exibição agrupada.
        """
        queryset = super().get_queryset(request)
        return get_object_or_404(RegistroEvolucao, pk=object_id)

    def get_aluno_nome(self, obj):
        """
        Gera o link correto para o nome do aluno:
        - Lista inicial: redireciona para a lista de evoluções do aluno.
        - Lista filtrada: redireciona para o detalhe da evolução.
        """
        if not obj.neurodivergente:
            return '-'

        if hasattr(self, 'request') and 'neurodivergente__id__exact' not in self.request.GET:
            # Link para a lista de evoluções do aluno
            url = f"{reverse('admin:neurodivergentes_registroevolucao_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
        else:
            # Link para o detalhe da evolução
            url = reverse('admin:neurodivergentes_registroevolucao_change', args=[obj.id])

        nome_completo = f"{obj.neurodivergente.primeiro_nome} {obj.neurodivergente.ultimo_nome}"
        return format_html(
            '<a href="{}" style="color: #447e9b; text-decoration: none;">{}</a>',
            url,
            nome_completo
        )
    get_aluno_nome.short_description = 'Aluno/Paciente'
    get_aluno_nome.admin_order_field = 'neurodivergente__primeiro_nome'

    def get_total_evolucoes(self, obj):
        """
        Retorna o total de evoluções do aluno.
        """
        if not obj.neurodivergente:
            return '0'
        return obj.neurodivergente.registros_evolucao.count()
    get_total_evolucoes.short_description = 'Total de Evoluções'

    def get_ultima_evolucao(self, obj):
        """
        Retorna a data da última evolução formatada.
        """
        if not obj.neurodivergente:
            return '-'
        ultima = obj.neurodivergente.registros_evolucao.order_by('-data').first()
        return ultima.data.strftime('%d/%m/%Y') if ultima else '-'
    get_ultima_evolucao.short_description = 'Última Evolução'

    def get_view_button(self, obj):
        """
        Retorna o botão de visualização que leva para a lista de evoluções do aluno.
        """
        if not obj.neurodivergente:
            return ''
        
        url = f"{reverse('admin:neurodivergentes_registroevolucao_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
        return format_html(
            '<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-eye"></i> Ver Evoluções</a>',
            url
        )
    get_view_button.short_description = 'Ver Evoluções'

    def get_list_display(self, request):
        """
        Altera as colunas exibidas dependendo se estamos na lista inicial ou na lista de evoluções de um aluno.
        """
        if request.GET.get('neurodivergente__id__exact'):
            # Na página de evoluções do aluno
            return ['neurodivergente', 'get_data_formatada', 'descricao_resumida', 'profissional', 'tem_anexos', 'get_acoes']
        # Na página inicial
        return ['get_aluno_nome', 'get_total_evolucoes', 'get_ultima_evolucao', 'get_view_button']

    def get_data_formatada(self, obj):
        """
        Retorna a data no formato dd/mm/yy
        """
        return obj.data.strftime('%d/%m/%y')
    get_data_formatada.short_description = 'Data'
    get_data_formatada.admin_order_field = 'data'

    def tem_anexos(self, obj):
        return bool(obj.anexos)
    tem_anexos.boolean = True
    tem_anexos.short_description = 'Anexos'

    def descricao_resumida(self, obj):
        max_length = 50
        if len(obj.descricao) > max_length:
            return f"{obj.descricao[:max_length]}..."
        return obj.descricao
    descricao_resumida.short_description = 'Descrição'

    def get_acoes(self, obj):
        """
        Retorna os botões de ação para a lista de evoluções do aluno.
        """
        editar_url = reverse('admin:neurodivergentes_registroevolucao_change', args=[obj.id])
        
        return format_html(
            '<div class="btn-group">'
            '<a href="{}" class="btn btn-info btn-sm" title="Editar"><i class="fas fa-edit"></i></a>'
            '<button type="button" class="btn btn-primary btn-sm" onclick="imprimirEvolucao({})"><i class="fas fa-print"></i> Imprimir</button>'
            '</div>',
            editar_url, obj.id
        )
    get_acoes.short_description = 'Ações'

    def get_edit_button(self, obj):
        """
        Retorna o botão de edição para a lista de evoluções do aluno.
        """
        url = reverse('admin:neurodivergentes_registroevolucao_change', args=[obj.id])
        return format_html(
            '<a class="btn btn-info btn-sm" href="{}"><i class="fas fa-edit"></i> Editar</a>',
            url
        )
    get_edit_button.short_description = 'Editar'

    class Media:
        css = {
            'all': ('admin/css/neurodivergentes_forms.css',)
        }
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.mask.min.js',
            'js/neurodivergentes_admin.js',
        )

from django import forms



class ParecerAvaliativoAdminForm(forms.ModelForm):
    class Meta:
        model = ParecerAvaliativo
        fields = '__all__'
        widgets = {
            'neurodivergente': forms.Select(attrs={'class': 'vLargeTextField'}),
            'escola': forms.Select(attrs={'class': 'vLargeTextField'}),
            'data_avaliacao': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'vDateField'
                },
                format='%Y-%m-%d'
            ),
            'evolucao': forms.Textarea(attrs={
                'rows': 4,
                'class': 'vLargeTextField',
                'placeholder': 'Descreva a evolução do aluno'
            }),
            'profissional_responsavel': forms.Select(attrs={'class': 'vLargeTextField'}),
            'anexos': forms.ClearableFileInput(attrs={'class': 'vFileUploadField'})
        }

@admin.register(ParecerAvaliativo)
class ParecerAvaliativoAdmin(admin.ModelAdmin):
    form = ParecerAvaliativoAdminForm
    list_display = ['neurodivergente', 'idade', 'escola', 'data_avaliacao', 'tem_anexos']
    readonly_fields = ['idade', 'ver_graficos']
    list_filter = ['data_avaliacao', 'escola']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']
    
    fieldsets = [
        (None, {
            'fields': [
                'neurodivergente',
                'idade',
                'escola', 
                'data_avaliacao',
                'ver_graficos',
                'evolucao',
                'profissional_responsavel',
                'anexos'
            ]
        })
    ]

    def ver_graficos(self, obj):
        if obj and obj.pk:
            return format_html(
                '<a class="button" href="{}" target="_blank" style="margin-bottom: 10px;">'
                '<i class="fas fa-chart-bar"></i> Ver Gráficos</a>',
                reverse('neurodivergentes:parecer_graficos', args=[obj.pk])
            )
        return ''
    ver_graficos.short_description = ''
    
    def tem_anexos(self, obj):
        return bool(obj.anexos)
    tem_anexos.boolean = True
    tem_anexos.short_description = 'Anexos'

@admin.register(HistoricoEscolar)
class HistoricoEscolarAdmin(admin.ModelAdmin):
    list_display = ['neurodivergente', 'escola_atual', 'serie_atual', 'modalidade_ensino']
    list_filter = ['modalidade_ensino', 'serie_atual']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']

@admin.register(Anamnese)
class AnamneseAdmin(admin.ModelAdmin):
    list_display = ['neurodivergente', 'tipo_parto', 'prematuridade']
    list_filter = ['tipo_parto', 'prematuridade']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']
    formfield_overrides = {
        models.DateField: {'widget': forms.DateInput(attrs={'class': 'vDateField', 'type': 'date'})}
    }
    
@admin.register(PlanoEducacional)
class PlanoEducacionalAdmin(admin.ModelAdmin):
    form = PlanoEducacionalForm
    list_display = ['pdi', 'data_inicio', 'data_fim', 'pedagogo_responsavel']
    list_filter = ['data_inicio', 'pedagogo_responsavel']
    search_fields = ['pdi__neurodivergente__primeiro_nome', 'pdi__neurodivergente__ultimo_nome']
    inlines = [AdaptacaoCurricularInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('pdi', 'pedagogo_responsavel', 'data_inicio', 'data_fim')
        }),
        ('Detalhes do Plano', {
            'fields': ('objetivos', 'estrategias', 'recursos')
        }),
    )