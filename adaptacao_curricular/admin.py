from django.contrib import admin
from django import forms
from django.urls import path, reverse
from django.http import JsonResponse
from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils.html import format_html
from profissionais_app.models import Profissional
from .models import (
    BNCCDisciplina,
    BNCCHabilidade,
    AdaptacaoCurricularIndividualizada,
    AdaptacaoHabilidade
)

@admin.register(BNCCDisciplina)
class BNCCDisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(BNCCHabilidade)
class BNCCHabilidadeAdmin(admin.ModelAdmin):
    fields = ('disciplina', 'ano', 'trimestre', 'objeto_conhecimento', 'codigo', 'descricao')
    list_display = ('disciplina', 'ano', 'trimestre', 'objeto_conhecimento', 'codigo')
    list_filter = ('disciplina', 'ano', 'trimestre')
    search_fields = ('codigo', 'descricao', 'objeto_conhecimento')
    autocomplete_fields = ['disciplina']
    list_select_related = ['disciplina']

class AdaptacaoHabilidadeForm(forms.ModelForm):
    class Meta:
        model = AdaptacaoHabilidade
        fields = ('habilidade', 'descritivo_adaptacao')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configura o campo de habilidade
        self.fields['habilidade'].label = 'Buscar Habilidade'
        self.fields['habilidade'].widget.attrs.update({
            'class': 'select2-habilidade',
            'data-placeholder': 'Digite o código ou palavras-chave da habilidade',
            'style': 'width: 100%',
        })
        
        # Configura o campo de descrição
        self.fields['descritivo_adaptacao'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Descreva a adaptação curricular para esta habilidade'
        })
        
        # Configura o queryset inicial
        self.fields['habilidade'].queryset = BNCCHabilidade.objects.all().select_related('disciplina')
        
    def clean(self):
        cleaned_data = super().clean()
        if 'habilidade' in cleaned_data:
            habilidade = cleaned_data['habilidade']
            if not habilidade:
                raise forms.ValidationError('Por favor, selecione uma habilidade.')
        return cleaned_data

class AdaptacaoHabilidadeInline(admin.StackedInline):
    model = AdaptacaoHabilidade
    form = AdaptacaoHabilidadeForm
    extra = 1
    fields = ('habilidade', 'descritivo_adaptacao')
    can_delete = True
    show_change_link = True
    classes = ('adaptacao-inline',)
    template = 'admin/adaptacao_curricular/edit_inline/adaptacao_stacked.html'
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['habilidade'].widget.can_add_related = False
        formset.form.base_fields['habilidade'].widget.can_change_related = False
        return formset

@admin.register(AdaptacaoCurricularIndividualizada)
class AdaptacaoCurricularIndividualizadaAdmin(admin.ModelAdmin):
    search_fields = ['aluno__primeiro_nome', 'aluno__ultimo_nome', 'escola__nome']
    autocomplete_fields = ['aluno', 'escola', 'profissional_responsavel']
    inlines = [AdaptacaoHabilidadeInline]
    change_form_template = 'admin/adaptacao_curricular/adaptacaocurricularindividualizada/change_form.html'
    change_list_template = 'admin/neurodivergentes/aci/change_list_material_dashboard.html'
    list_display = ['get_aluno_nome', 'get_total_adaptacoes', 'get_ultima_adaptacao', 'get_view_button']
    list_filter = ['aluno', 'escola']
    list_per_page = 20

    def get_queryset(self, request):
        """
        Retorna apenas a adaptação mais recente por aluno na lista inicial,
        ou todas as adaptações se um filtro de aluno estiver ativo.
        """
        self.request = request
        queryset = super().get_queryset(request).select_related('aluno', 'escola')

        aluno_id = request.GET.get('aluno__id__exact')
        if aluno_id:
            # Lista todas as adaptações do aluno filtrado
            return queryset.filter(aluno_id=aluno_id).order_by('-data_cadastro')

        # Lista inicial: retorna apenas a adaptação mais recente por aluno
        latest_adaptacao_ids = queryset.values('aluno').annotate(
            max_id=models.Max('id')
        ).values_list('max_id', flat=True)

        return queryset.filter(id__in=latest_adaptacao_ids).order_by('aluno__primeiro_nome')

    def get_list_display(self, request):
        """
        Altera as colunas exibidas dependendo se estamos na lista inicial
        ou na lista de adaptações de um aluno.
        """
        if request.GET.get('aluno__id__exact'):
            # Lista de adaptações do aluno
            return ['get_aluno_nome', 'escola', 'data_cadastro', 'get_acoes']
        # Lista inicial
        return ['get_aluno_nome', 'get_total_adaptacoes', 'get_ultima_adaptacao', 'get_view_button']

    def get_aluno_nome(self, obj):
        """
        Retorna o nome do aluno.
        """
        if not obj.aluno:
            return '-'
        return f"{obj.aluno.primeiro_nome} {obj.aluno.ultimo_nome}"
    get_aluno_nome.short_description = 'Aluno'
    get_aluno_nome.admin_order_field = 'aluno__primeiro_nome'

    def get_total_adaptacoes(self, obj):
        """
        Retorna o total de adaptações do aluno.
        """
        if not obj.aluno:
            return '0'
        return AdaptacaoCurricularIndividualizada.objects.filter(aluno=obj.aluno).count()
    get_total_adaptacoes.short_description = 'Total de Adaptações'

    def get_ultima_adaptacao(self, obj):
        """
        Retorna a data da última adaptação do aluno.
        """
        if not obj.aluno:
            return '-'
        ultima = AdaptacaoCurricularIndividualizada.objects.filter(
            aluno=obj.aluno
        ).order_by('-data_cadastro').first()
        return ultima.data_cadastro if ultima else '-'
    get_ultima_adaptacao.short_description = 'Última Adaptação'
    get_ultima_adaptacao.admin_order_field = 'data_cadastro'

    def get_view_button(self, obj):
        """
        Retorna o botão de visualização que leva para a lista de adaptações do aluno.
        """
        if not obj.aluno:
            return '-'
        url = f"{reverse('admin:adaptacao_curricular_adaptacaocurricularindividualizada_changelist')}?aluno__id__exact={obj.aluno.id}"
        return format_html(
            '<a class="button" href="{}" style="white-space: nowrap;">'
            '<i class="fas fa-eye" style="margin-right: 4px;"></i>Ver Adaptações</a>',
            url
        )
    get_view_button.short_description = 'Ver Adaptações'

    def get_acoes(self, obj):
        """
        Retorna os botões de ação para a lista de adaptações do aluno.
        """
        edit_url = reverse('admin:adaptacao_curricular_adaptacaocurricularindividualizada_change', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="white-space: nowrap;">'
            '<i class="fas fa-edit" style="margin-right: 4px;"></i>Editar</a>',
            edit_url
        )
    get_acoes.short_description = 'Ações'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
            )
        }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj:
            # Agrupa adaptações por disciplina
            adaptacoes_por_disciplina = {}
            for adaptacao in obj.adaptacoes.select_related('habilidade__disciplina').all():
                disciplina = adaptacao.habilidade.disciplina
                if disciplina not in adaptacoes_por_disciplina:
                    adaptacoes_por_disciplina[disciplina] = []
                adaptacoes_por_disciplina[disciplina].append(adaptacao)
            
            # Cria os botões para cada disciplina
            disciplina_buttons = [{
                'nome': disciplina.nome,
                'id': disciplina.id,
                'url': reverse('adaptacao_curricular:imprimir_adaptacao_disciplina', 
                              args=[obj.id, disciplina.id])
            } for disciplina in adaptacoes_por_disciplina.keys()]
            
            extra_context['disciplina_buttons'] = disciplina_buttons
        
        return super().change_view(request, object_id, form_url, extra_context)
    def buscar_habilidades(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
            
        term = request.GET.get('term', '')
        results = []
        
        if term:
            habilidades = BNCCHabilidade.objects.filter(
                models.Q(codigo__icontains=term) |
                models.Q(descricao__icontains=term) |
                models.Q(objeto_conhecimento__icontains=term)
            ).select_related('disciplina')[:10]
            
            for hab in habilidades:
                results.append({
                    'id': hab.id,
                    'text': f'{hab.codigo} - {hab.disciplina.nome}',
                    'codigo': hab.codigo,
                    'disciplina': hab.disciplina.nome,
                    'ano': hab.ano,
                    'trimestre': hab.trimestre,
                    'objeto_conhecimento': hab.objeto_conhecimento,
                    'descricao': hab.descricao
                })
        
        return JsonResponse({'results': results}, safe=False)
        
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('buscar-habilidades/', self.buscar_habilidades, name='buscar_habilidades'),
        ]
        return custom_urls + urls


    fieldsets = [
        ('Informações do Aluno', {
            'fields': ['aluno', 'escola', 'modalidade_ensino', 'ano', 'trimestre', 'profissional_responsavel']
        }),
    ]
    list_display = ('aluno', 'escola', 'profissional_responsavel', 'data_cadastro')
    list_filter = ('escola', 'data_cadastro')
    search_fields = (
        'aluno__primeiro_nome',
        'aluno__ultimo_nome',
        'escola__nome',
        'profissional_responsavel__nome'
    )
    autocomplete_fields = ['aluno', 'escola', 'profissional_responsavel']
    inlines = [AdaptacaoHabilidadeInline]
    
    class Media:
        css = {
            'all': (
                'admin/css/forms.css',
                'admin/css/widgets.css',
                'admin/css/vendor/select2/select2.min.css',
                'admin/css/autocomplete.css',
                'adaptacao_curricular/css/adaptacao.css',
            )
        }
        js = (
            'admin/js/vendor/select2/select2.full.min.js',
            'admin/js/vendor/select2/i18n/pt-BR.js',
            'admin/js/jquery.init.js',
            'admin/js/autocomplete.js',
            'adaptacao_curricular/js/adaptacao.js',
        )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Se é um novo objeto
            try:
                profissional = Profissional.objects.get(user=request.user)
                form.base_fields['profissional_responsavel'].initial = profissional
            except Profissional.DoesNotExist:
                pass
        return form
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            try:
                profissional = Profissional.objects.get(user=request.user)
                if not obj.profissional_responsavel:
                    obj.profissional_responsavel = profissional
            except Profissional.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('buscar-habilidades/',
                 self.admin_site.admin_view(self.buscar_habilidades),
                 name='buscar_habilidades'),
        ]
        return custom_urls + urls
    
    def buscar_habilidades(self, request):
        """Endpoint para buscar habilidades baseado no termo de busca."""
        if not request.user.is_staff:
            raise PermissionDenied
            
        term = request.GET.get('term', '')
        print(f'Termo de busca recebido: {term}')
        
        try:
            # Primeiro tenta buscar por ID
            if term.isdigit():
                habilidade = BNCCHabilidade.objects.select_related('disciplina').filter(id=term).first()
                if habilidade:
                    results = [{
                        'id': habilidade.id,
                        'codigo': habilidade.codigo,
                        'disciplina': habilidade.disciplina.nome if habilidade.disciplina else '',
                        'ano': habilidade.get_ano_display() if hasattr(habilidade, 'get_ano_display') else str(habilidade.ano),
                        'trimestre': habilidade.get_trimestre_display() if hasattr(habilidade, 'get_trimestre_display') else str(habilidade.trimestre),
                        'objeto_conhecimento': habilidade.objeto_conhecimento,
                        'descricao': habilidade.descricao,
                        'text': habilidade.codigo  # Campo obrigatório para o Select2
                    }]
                    return JsonResponse({'results': results})
            
            # Se não for ID ou não encontrar, busca por outros campos
            habilidades = BNCCHabilidade.objects.select_related('disciplina').filter(
                models.Q(codigo__icontains=term) |
                models.Q(objeto_conhecimento__icontains=term) |
                models.Q(descricao__icontains=term) |
                models.Q(ano__icontains=term) |
                models.Q(trimestre__icontains=term) |
                models.Q(disciplina__nome__icontains=term)
            ).order_by('disciplina__nome', 'ano', 'trimestre', 'codigo')[:20]  # Limita a 20 resultados
            
            print(f'Habilidades encontradas: {habilidades.count()}')
            
            results = [{
                'id': h.id,
                'codigo': h.codigo,
                'disciplina': h.disciplina.nome if h.disciplina else '',
                'ano': h.get_ano_display() if hasattr(h, 'get_ano_display') else str(h.ano),
                'trimestre': h.get_trimestre_display() if hasattr(h, 'get_trimestre_display') else str(h.trimestre),
                'objeto_conhecimento': h.objeto_conhecimento,
                'descricao': h.descricao,
                'text': h.codigo  # Campo obrigatório para o Select2
            } for h in habilidades]
            
            return JsonResponse({'results': results})
            
        except Exception as e:
            print(f'Erro ao buscar habilidades: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)
            print(f'Erro ao buscar habilidades: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

        js = (
            'admin/js/jquery.init.js',
            'admin/js/core.js',
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/vendor/select2/select2.full.js',
            'admin/js/adaptacao.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['profissional_responsavel'].initial = request.user
        return form

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('buscar-habilidades/',
                 self.admin_site.admin_view(self.buscar_habilidades),
                 name='buscar_habilidades'),
        ]
        return custom_urls + urls

    def buscar_habilidades(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Não autorizado'}, status=403)

        term = request.GET.get('term', '')
        if not term:
            return JsonResponse({'results': []}, safe=False)

        habilidades = BNCCHabilidade.objects.filter(
            models.Q(codigo__icontains=term) |
            models.Q(descricao__icontains=term) |
            models.Q(objeto_conhecimento__icontains=term)
        ).select_related('disciplina')[:20]

        results = [{
            'id': h.id,
            'text': f'{h.codigo} - {h.descricao[:100]}...',
            'codigo': h.codigo,
            'disciplina': h.disciplina.nome,
            'ano': dict(h.ANOS_CHOICES)[h.ano],
            'trimestre': dict(h.TRIMESTRE_CHOICES)[h.trimestre],
            'objeto_conhecimento': h.objeto_conhecimento,
            'descricao': h.descricao
        } for h in habilidades]

        return JsonResponse({'results': results}, safe=False)

    def get_anos(self, request, disciplina_id):
        anos = BNCCHabilidade.objects.filter(
            disciplina_id=disciplina_id
        ).values_list('ano', flat=True).distinct().order_by('ano')
        anos_list = [{'id': ano, 'text': dict(BNCCHabilidade.ANOS_CHOICES)[ano]} for ano in anos]
        return JsonResponse(anos_list, safe=False)

    def get_trimestres(self, request, disciplina_id, ano):
        trimestres = BNCCHabilidade.objects.filter(
            disciplina_id=disciplina_id,
            ano=ano
        ).values_list('trimestre', flat=True).distinct().order_by('trimestre')
        trimestres_list = [{'id': tri, 'text': dict(BNCCHabilidade.TRIMESTRE_CHOICES)[tri]} for tri in trimestres]
        return JsonResponse(trimestres_list, safe=False)

    def get_habilidades(self, request, disciplina_id, ano, trimestre):
        habilidades = BNCCHabilidade.objects.filter(
            disciplina_id=disciplina_id,
            ano=ano,
            trimestre=trimestre
        ).values('id', 'codigo', 'objeto_conhecimento', 'descricao')
        return JsonResponse(list(habilidades), safe=False)
