from django import forms
import requests
from django.utils import timezone
from .models import (
    Neurodivergente, GrupoFamiliar, Neurodivergencia,
    PDI, PlanoEducacional,
    AdaptacaoCurricular, RegistroEvolucao,
    Monitoramento, Frequencia, ParecerAvaliativo
)

class NeurodivergenteForms(forms.ModelForm):
    class Meta:
        model = Neurodivergente
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        cep = ''.join(filter(str.isdigit, cep))
        if len(cep) != 8:
            raise forms.ValidationError('CEP inválido.')
        
        # Formata o CEP
        cep_formatado = f'{cep[:5]}-{cep[5:]}'
        
        # Consulta o CEP na API
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            data = response.json()
            
            if not data.get('erro'):
                # Atualiza os campos com os dados do CEP
                self.cleaned_data['endereco'] = data.get('logradouro', '')
                self.cleaned_data['bairro'] = data.get('bairro', '')
                self.cleaned_data['cidade'] = data.get('localidade', '')
                self.cleaned_data['estado'] = data.get('uf', '').upper()
        except:
            pass  # Silently fail if API is unavailable
        
        return cep_formatado

class GrupoFamiliarForm(forms.ModelForm):
    class Meta:
        model = GrupoFamiliar
        fields = '__all__'
        widgets = {
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }

class NeurodivergenciaForm(forms.ModelForm):
    class Meta:
        model = Neurodivergencia
        fields = '__all__'
        widgets = {
            'data_diagnostico': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }

class PDIForm(forms.ModelForm):
    class Meta:
        model = PDI
        fields = '__all__'
        widgets = {
            'data_criacao': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'meta': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva a meta ou habilidade a ser desenvolvida'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Observações adicionais sobre o PDI'
            })
        }

class PlanoEducacionalForm(forms.ModelForm):
    class Meta:
        model = PlanoEducacional
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_fim': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'objetivos': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva os objetivos do plano'
            }),
            'estrategias': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva as estratégias a serem utilizadas'
            }),
            'recursos': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Liste os recursos necessários'
            })
        }

class AdaptacaoCurricularForm(forms.ModelForm):
    class Meta:
        model = AdaptacaoCurricular
        fields = '__all__'
        widgets = {
            'data_inicio': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_fim': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'conteudo_adaptado': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o conteúdo adaptado'
            }),
            'estrategias': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva as estratégias de ensino'
            }),
            'recursos': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Liste os recursos didáticos necessários'
            }),
            'avaliacao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva o processo avaliativo'
            })
        }

class RegistroEvolucaoForm(forms.ModelForm):
    class Meta:
        model = RegistroEvolucao
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva a evolução observada'
            })
        }

class MonitoramentoForm(forms.ModelForm):
    class Meta:
        model = Monitoramento
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'meta': forms.TextInput(attrs={
                'placeholder': 'Meta ou habilidade monitorada'
            }),
            'observacoes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Observações sobre o progresso'
            })
        }

class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = '__all__'
        widgets = {
            'observacoes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Observações sobre a frequência'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Anos de 2000 até 2050
        anos = range(2000, 2051)
        self.fields['ano'].widget = forms.Select(choices=[
            (ano, ano) for ano in anos
        ])

    def clean_ano(self):
        ano = self.cleaned_data.get('ano')
        ano_atual = timezone.now().year
        
        if ano > ano_atual:
            raise ValidationError('Não é permitido registrar frequência para anos futuros.')
        
        return ano

class ParecerAvaliativoForm(forms.ModelForm):
    class Meta:
        model = ParecerAvaliativo
        fields = '__all__'
        widgets = {
            'data_avaliacao': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'evolucao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva a evolução do aluno'
            }),
            'pontos_fortes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Liste os pontos fortes observados'
            }),
            'desafios': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva os desafios identificados'
            }),
            'recomendacoes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Liste as recomendações'
            }),
            'conclusoes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Apresente as conclusões'
            })
        }