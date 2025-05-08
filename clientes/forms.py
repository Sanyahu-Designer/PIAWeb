from django import forms
from .models import Cliente
from django.contrib.auth.models import User, Group
from .models_profile import Profile

class ClienteForm(forms.ModelForm):
    estado_choices = [
        ('', 'Selecionar'),
        ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
        ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
        ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
        ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
        ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
        ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
        ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].widget = forms.Select(choices=self.estado_choices)

    class Meta:
        model = Cliente
        fields = [
            'nome', 'cnpj', 'slug', 'inscricao_estadual', 
            'logradouro', 'numero', 'complemento', 'bairro', 
            'cidade', 'estado', 'cep', 
            'telefone_principal', 'email_principal',
            'nome_responsavel_financeiro', 'cargo_responsavel_financeiro', 
            'email_responsavel_financeiro', 'telefone_responsavel_financeiro',
            'numero_habitantes', 'numero_escolas', 'numero_alunos',
            'ativo',
            'nome_prefeito', 'nome_vice_prefeito',
            'nome_secretario_saude', 'nome_secretario_educacao',
            'email_secretario_saude', 'telefone_secretario_saude',
            'email_secretario_educacao', 'telefone_secretario_educacao',
        ]
        widgets = {
            'ativo': forms.CheckboxInput(),
        }

class PrimeiroUsuarioForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="Primeiro nome", max_length=30)
    last_name = forms.CharField(label="Último nome", max_length=150)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data

class EditarClienteUsuarioForm(forms.Form):
    username = forms.CharField(label="Usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="Primeiro nome", max_length=30)
    last_name = forms.CharField(label="Último nome", max_length=150)
    password = forms.CharField(label="Nova senha", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirme a nova senha", widget=forms.PasswordInput, required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password or password2:
            if password != password2:
                self.add_error("password2", "As senhas não coincidem.")
        return cleaned_data
