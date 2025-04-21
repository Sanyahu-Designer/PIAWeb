from django.contrib import admin
from django.utils.html import format_html
from .models import ConfiguracaoCliente

# Register your models here.

@admin.register(ConfiguracaoCliente)
class ConfiguracaoClienteAdmin(admin.ModelAdmin):
    """
    Configuração da interface administrativa para o modelo ConfiguracaoCliente.
    """
    fieldsets = (
        ('Dados Institucionais', {
            'fields': (
                'logomarca',
                'logomarca_preview',
                ('nome_municipio', 'cnpj'),
                ('endereco', 'bairro'),
                ('cidade', 'estado'),
                ('cep', 'telefone_geral'),
                ('email_institucional', 'site_oficial'),
                ('facebook', 'instagram'),  # Garantindo que os campos de redes sociais estejam agrupados corretamente em uma tupla
            ),
            'classes': ('fieldset-container',),
        }),
        ('Dados das Autoridades', {
            'fields': (
                ('nome_prefeito', 'nome_vice_prefeito'),
                ('nome_secretario_saude', 'nome_secretario_educacao'),
            ),
            'classes': ('fieldset-container',),
        }),
    )
    
    list_display = ('nome_municipio', 'cnpj', 'logomarca_preview', 'nome_prefeito', 'data_atualizacao', 'acoes')
    search_fields = ('nome_municipio', 'cnpj', 'nome_prefeito')
    readonly_fields = ('data_atualizacao', 'logomarca_preview')
    
    # Templates personalizados
    change_form_template = 'admin/configuracoes/configuracaocliente/change_form.html'
    add_form_template = 'admin/configuracoes/configuracaocliente/change_form.html'
    change_list_template = 'admin/configuracoes/configuracaocliente/change_list.html'
    
    def acoes(self, obj):
        """
        Botões de ação para cada registro na lista.
        """
        from django.urls import reverse
        url = reverse('admin:configuracoes_configuracaocliente_change', args=[obj.id])
        return format_html(
            '<a href="{}" class="btn btn-outline-primary btn-sm mb-0" title="Editar">'
            '<i class="material-symbols-rounded opacity-10" style="font-size: 16px;">edit</i> Editar</a>',
            url
        )
    
    acoes.short_description = 'Ações'
    
    def has_delete_permission(self, request, obj=None):
        """
        Desabilita a exclusão de configurações, permitindo apenas edição.
        """
        return False
    
    def has_add_permission(self, request):
        """
        Verifica se já existe uma configuração antes de permitir adicionar nova.
        """
        # Temporariamente permitindo adicionar independente do número de configurações existentes
        return True
        
    def response_change(self, request, obj):
        if "_save" in request.POST:
            from django.urls import reverse
            from django.http import HttpResponseRedirect
            # Redireciona para o dashboard (ajuste o nome da URL caso necessário)
            return HttpResponseRedirect(reverse('dashboard'))
        return super().response_change(request, obj)

    class Media:
        js = ('admin/js/configuracoes.js',)
        css = {
            'all': ('admin/css/configuracoes.css',)
        }
