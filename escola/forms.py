from django import forms
from .models import Escola
import requests

class EscolaForm(forms.ModelForm):
    class Meta:
        model = Escola
        fields = '__all__'
        labels = {
            'telefone': 'Celular/Whatsapp'  # Atualiza o label do campo "telefone"
        }
        widgets = {
            'telefone': forms.TextInput(attrs={
                'data-mask': '(00) 00000-0000'
            }),
            'cep': forms.TextInput(attrs={
                'data-mask': '00000-000'
            }),
            'estado': forms.Select(attrs={
                'class': 'select2'  # Adiciona classe para melhor estilização
            }),
            'profissionais_educacao': forms.SelectMultiple(
                attrs={
                    'class': 'select2-multiple',
                    'data-placeholder': 'Selecione os profissionais da educação'
                }
            ),
            'profissionais_saude': forms.SelectMultiple(
                attrs={
                    'class': 'select2-multiple',
                    'data-placeholder': 'Selecione os profissionais da saúde'
                }
            )
        }

    def clean_codigo_inep(self):
        codigo = self.cleaned_data['codigo_inep']
        if not codigo.isdigit() or len(codigo) != 8:
            raise forms.ValidationError(
                'O código INEP deve conter exatamente 8 dígitos numéricos.'
            )
        return codigo

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        telefone = ''.join(filter(str.isdigit, telefone))
        if len(telefone) != 11:
            raise forms.ValidationError(
                'O telefone deve conter 11 dígitos numéricos.'
            )
        return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'

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