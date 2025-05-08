from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profissional
from .forms import ProfissionalForm
from django import forms

class ProfissionalInline(admin.StackedInline):
    model = Profissional
    form = ProfissionalForm
    can_delete = False
    verbose_name_plural = 'Profissional'
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'foto_perfil', 'foto_preview', 'celular',
                'data_nascimento', 'genero'
            ),
            'classes': ('tab-dados-pessoais',)
        }),
        ('Qualificação Profissional', {
            'fields': (
                'profissao', 'especialidade', 'registro_profissional',
                'estado_registro', 'formacao', 'experiencia_neurodiversidade'
            ),
            'classes': ('tab-qualificacao',)
        }),
        ('Endereço', {
            'fields': (
                'cep', 'endereco', 'numero', 'complemento',
                'bairro', 'cidade', 'estado'
            ),
            'classes': ('tab-endereco',)
        }),
        ('Outros', {
            'fields': (
                'biografia', 'facebook', 'instagram'
            ),
            'classes': ('tab-outros',)
        }),
    )

    readonly_fields = ['foto_preview']

    class Media:
        css = {
            'all': ('admin/css/profissionais_forms.css',)
        }
        js = (
            'admin/js/jquery.mask.min.js',
            'admin/js/profissionais_admin.js',
            'admin/js/cep_autocomplete.js',
        )

class ProfissionalAdminForm(forms.ModelForm):
    # Campos do usuário
    first_name = forms.CharField(label="Nome", max_length=30, required=True)
    last_name = forms.CharField(label="Sobrenome", max_length=150, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    username = forms.CharField(label="Usuário", max_length=150, required=True)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput, required=False)
    # Campo estado como ChoiceField (menu suspenso)
    estado = forms.ChoiceField(
        choices=[('', 'Selecionar')] + list(Profissional.ESTADOS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    celular = forms.CharField(label="Celular/WhatsApp", max_length=15, required=True)
    genero = forms.ChoiceField(label="Gênero", choices=[('M', 'Masculino'), ('F', 'Feminino')], required=True)
    data_nascimento = forms.DateField(label="Data de Nascimento", required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profissional
        exclude = ['user']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajuste obrigatoriedade correta dos campos
        self.fields['celular'].required = True
        self.fields['genero'].required = True
        self.fields['data_nascimento'].required = False
        self.fields['foto_perfil'].required = False
        # Campos de Endereço não obrigatórios
        self.fields['cep'].required = False
        self.fields['endereco'].required = False
        self.fields['numero'].required = False
        self.fields['complemento'].required = False
        self.fields['bairro'].required = False
        self.fields['cidade'].required = False
        self.fields['estado'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password or password2:
            if password != password2:
                self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data

@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):
    form = ProfissionalAdminForm
    list_display = ['get_nome_completo', 'get_profissao', 'celular', 'cidade', 'estado']
    list_filter = ['profissao', 'estado', 'experiencia_neurodiversidade']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'celular']
    ordering = ['user__first_name', 'user__last_name']

    fieldsets = (
        ('Dados Pessoais', {
            'fields': (
                'first_name', 'last_name', 'email',
                'foto_perfil', 'foto_preview', 'celular',
                'data_nascimento', 'genero'
            ),
            'classes': ('tab-dados-pessoais',)
        }),
        ('Usuário', {
            'fields': (('username', 'password', 'password2'),),
            'description': 'Preencha os dados de acesso do usuário que será associado ao profissional.'
        }),
        ('Qualificação Profissional', {
            'fields': (
                'profissao', 'especialidade', 'registro_profissional',
                'estado_registro', 'formacao', 'experiencia_neurodiversidade'
            ),
            'classes': ('tab-qualificacao',)
        }),
        ('Endereço', {
            'fields': (
                'cep', 'endereco', 'numero', 'complemento',
                'bairro', 'cidade', 'estado'
            ),
            'classes': ('tab-endereco',)
        }),
        ('Outros', {
            'fields': (
                'biografia', 'facebook', 'instagram'
            ),
            'classes': ('tab-outros',)
        }),
    )

    readonly_fields = ['foto_preview']

    def save_model(self, request, obj, form, change):
        # Cria ou atualiza o usuário associado
        data = form.cleaned_data
        if not obj.user_id:
            user = User(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            if data.get('password'):
                user.set_password(data['password'])
            else:
                user.set_unusable_password()
            user.save()
            obj.user = user
        else:
            user = obj.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            user.username = data['username']
            if data.get('password'):
                user.set_password(data['password'])
            user.save()
        super().save_model(request, obj, form, change)

    def get_nome_completo(self, obj):
        return obj.user.get_full_name()
    get_nome_completo.short_description = 'Nome'
    get_nome_completo.admin_order_field = 'user__first_name'

    def get_profissao(self, obj):
        return obj.get_profissao_display()
    get_profissao.short_description = 'Profissão'
    get_profissao.admin_order_field = 'profissao'

    class Media:
        css = {
            'all': ('admin/css/profissionais_forms.css',)
        }
        js = (
            'admin/js/jquery.mask.min.js',
            'admin/js/profissionais_admin.js',
            'admin/js/cep_autocomplete.js',
        )