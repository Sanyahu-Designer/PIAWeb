from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class ConfiguracaoCliente(models.Model):
    """
    Modelo para armazenar as configurações do cliente (município/prefeitura).
    Inclui dados institucionais e informações sobre autoridades.
    """
    # Dados Institucionais
    logomarca = models.ImageField('Logomarca', upload_to='configuracoes/logomarca/', 
                                 help_text='Imagem do brasão oficial (formato recomendado: PNG, dimensões ideais 120x120px ou 150x100px, fundo transparente) para uso no cabeçalho dos relatórios', 
                                 blank=True, null=True)
    nome_municipio = models.CharField('Nome da Prefeitura', max_length=100)
    cnpj = models.CharField('CNPJ da prefeitura', max_length=18)
    endereco = models.CharField('Endereço', max_length=255)
    bairro = models.CharField('Bairro', max_length=100, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True, null=True)
    estado = models.CharField('Estado', max_length=2, blank=True, null=True)
    cep = models.CharField('CEP', max_length=9, blank=True, null=True)
    telefone_geral = models.CharField('Telefone', max_length=20, blank=True, null=True)
    email_institucional = models.EmailField('E-mail institucional', blank=True, null=True)
    site_oficial = models.CharField('Site oficial', max_length=255, blank=True, null=True)
    facebook = models.CharField('Facebook', max_length=255, blank=True, null=True)
    instagram = models.CharField('Instagram', max_length=255, blank=True, null=True)
    
    # Dados das Autoridades
    nome_prefeito = models.CharField('Nome do prefeito(a)', max_length=100)
    nome_vice_prefeito = models.CharField('Nome do vice-prefeito(a)', max_length=100, blank=True, null=True)
    nome_secretario_saude = models.CharField('Nome do Secretário municipal da Saúde', max_length=100, blank=True, null=True)
    nome_secretario_educacao = models.CharField('Nome do Secretário municipal da Educação', max_length=100, blank=True, null=True)
    
    data_atualizacao = models.DateTimeField('Data de Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração da Prefeitura'
        verbose_name_plural = 'Configurações da Prefeitura'
    
    def __str__(self):
        return f"Configuração: {self.nome_municipio}"
    
    def logomarca_preview(self):
        if self.logomarca:
            return mark_safe(
                f'<img src="{self.logomarca.url}" width="150" alt="Logomarca" />'
            )
        return "Sem logomarca"
    logomarca_preview.short_description = 'Visualização da Logomarca'
