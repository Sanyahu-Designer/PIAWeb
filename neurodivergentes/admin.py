from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Count, Max, Subquery, OuterRef, Avg
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from escola.models import ModalidadeEnsino, ProgramaEducacional, Recurso, Escola
from escola.forms import EscolaForm
from .models import (
    Neurodivergente, GrupoFamiliar, HistoricoEscolar,
    Neurodivergencia, CondicaoNeurodivergente,
    CategoriaNeurodivergente, DiagnosticoNeurodivergente,
    Anamnese, PDI, MetaHabilidade, PDIMetaHabilidade,
    PlanoEducacional, AdaptacaoCurricular, RegistroEvolucao,
    Monitoramento, Frequencia, ParecerAvaliativo
)
from .forms import (
    NeurodivergenteForms, PDIForm, PlanoEducacionalForm,
    AdaptacaoCurricularForm, RegistroEvolucaoForm,
    MonitoramentoForm, FrequenciaForm, ParecerAvaliativoForm
)

from django.db.models import Max

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
        self.request = request
        queryset = super().get_queryset(request).select_related(
            'neurodivergente', 
            'pedagogo_responsavel'
        ).prefetch_related('metas_habilidades')
        
        neurodivergente_id = request.GET.get('neurodivergente__id__exact')
        if neurodivergente_id:
            # Se um aluno específico foi selecionado, mostra todos os seus PDIs
            return queryset.filter(
                neurodivergente_id=neurodivergente_id
            ).order_by('-data_criacao')
        
        # Na tela inicial, mostra apenas um PDI por aluno (agrupamento)
        from django.db.models import Max
        latest_pdis = queryset.values('neurodivergente').annotate(
            max_id=Max('id')
        ).values('max_id')
        
        return queryset.filter(id__in=latest_pdis).order_by(
            'neurodivergente__primeiro_nome'
        )

    def get_aluno_nome(self, obj):
        if not obj.neurodivergente:
            return '-'
            
        if hasattr(self, 'request') and 'neurodivergente__id__exact' in self.request.GET:
            url = reverse('admin:neurodivergentes_pdi_change', args=[obj.id])
        else:
            url = f"{reverse('admin:neurodivergentes_pdi_changelist')}?neurodivergente__id__exact={obj.neurodivergente.id}"
            
        nome_completo = f"{obj.neurodivergente.primeiro_nome} {obj.neurodivergente.ultimo_nome}"
        return format_html(
            '<a href="{}" style="color: #447e9b; text-decoration: none;">{}</a>',
            url,
            nome_completo
        )
    get_aluno_nome.short_description = 'Aluno/Paciente'
    get_aluno_nome.admin_order_field = 'neurodivergente__primeiro_nome'

    def get_total_pdis(self, obj):
        if not obj.neurodivergente:
            return 0
        return PDI.objects.filter(neurodivergente=obj.neurodivergente).count()
    get_total_pdis.short_description = 'Total de PDIs'

    def get_ultimo_pdi(self, obj):
        return obj.data_criacao if obj.data_criacao else '-'
    get_ultimo_pdi.short_description = 'Último PDI'

    def changelist_view(self, request, extra_context=None):
        self.request = request
        if 'neurodivergente__id__exact' in request.GET:
            self.list_display = ['get_aluno_nome', 'data_criacao', 'get_progresso', 'status', 'get_view_button']
        else:
            self.list_display = ['get_aluno_nome', 'get_total_pdis', 'get_ultimo_pdi', 'get_view_button']
        return super().changelist_view(request, extra_context)

    def get_progresso(self, obj):
        metas = obj.metas_habilidades.all()
        if not metas:
            return '0%'
        total_progresso = sum(meta.progresso for meta in metas)
        media_progresso = total_progresso / len(metas)
        return f'{int(media_progresso)}%'
    get_progresso.short_description = 'Progresso (%)'

    def get_view_button(self, obj):
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
    list_display = ['neurodivergente', 'data', 'meta', 'nivel']
    list_filter = ['data', 'nivel']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']

@admin.register(RegistroEvolucao)
class RegistroEvolucaoAdmin(admin.ModelAdmin):
    form = RegistroEvolucaoForm
    list_display = ['neurodivergente', 'data', 'profissional', 'tem_anexos']
    list_filter = ['data', 'profissional']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']

    def tem_anexos(self, obj):
        return bool(obj.anexos)
    tem_anexos.boolean = True
    tem_anexos.short_description = 'Anexos'

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    form = FrequenciaForm
    list_display = ['neurodivergente', 'ano', 'get_mes_display', 'total_atendimentos']
    list_filter = ['ano', 'mes']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']

@admin.register(ParecerAvaliativo)
class ParecerAvaliativoAdmin(admin.ModelAdmin):
    form = ParecerAvaliativoForm
    list_display = ['neurodivergente', 'escola', 'data_avaliacao', 'tem_anexos']
    list_filter = ['data_avaliacao', 'escola']
    search_fields = ['neurodivergente__primeiro_nome', 'neurodivergente__ultimo_nome']

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