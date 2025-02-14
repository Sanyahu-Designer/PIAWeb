from django.contrib import admin
from django import forms
from django.urls import path
from django.http import JsonResponse
from django.db import models
from django.core.exceptions import PermissionDenied
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
    show_change_link = False
    classes = ('adaptacao-inline',)
    template = 'admin/adaptacao_curricular/edit_inline/stacked.html'
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        return formset

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['habilidade'].widget.can_add_related = False
        formset.form.base_fields['habilidade'].widget.can_change_related = False
        return formset

@admin.register(AdaptacaoCurricularIndividualizada)
class AdaptacaoCurricularIndividualizadaAdmin(admin.ModelAdmin):
    search_fields = ['aluno__primeiro_nome', 'aluno__ultimo_nome', 'escola__nome']
    autocomplete_fields = ['aluno', 'escola', 'profissional_responsavel']
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
                'admin/css/adaptacao.css',
            )
        }
        js = (
            'admin/js/vendor/select2/select2.full.min.js',
            'admin/js/vendor/select2/i18n/pt-BR.js',
            'admin/js/jquery.init.js',
            'admin/js/autocomplete.js',
            'admin/js/adaptacao.js',
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
