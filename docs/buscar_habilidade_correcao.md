# Documentação: Correção do Campo "Buscar Habilidade"

Esta documentação descreve o processo de correção do campo "Buscar Habilidade" no card Habilidades da página de edição do PEI (antigo ACI).

## Problema Identificado

O campo "Buscar Habilidade" deixou de buscar os dados corretamente. Ao analisar o código, identificamos que o problema estava relacionado à URL incorreta que estava sendo usada para buscar as habilidades.

## Solução Implementada

### 1. Correção da URL no JavaScript

A principal correção foi feita no arquivo JavaScript que controla o campo "Buscar Habilidade". A URL estava incorreta e foi atualizada para apontar para o endpoint correto:

```javascript
// Antes
const apiUrl = '/dashboard/adaptacao_curricular/adaptacaocurricularindividualizada/buscar-habilidades/';

// Depois
const apiUrl = '/dashboard/admin/adaptacao_curricular/adaptacaocurricularindividualizada/buscar-habilidades/';
```

O problema estava no caminho da URL, que não incluía o segmento `/admin/` necessário para acessar corretamente o endpoint no Django Admin.

### 2. Organização do Código no Admin.py

Também organizamos o código no arquivo `admin.py` para garantir que o método `buscar_habilidades` estivesse corretamente configurado e acessível pela URL. Isso incluiu:

1. Remover duplicações do método `buscar_habilidades`
2. Garantir que a URL estivesse corretamente registrada em `get_urls`
3. Manter a implementação correta do método que retorna os resultados da busca

```python
def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
        path('get_habilidade_details/', self.admin_site.admin_view(self.get_habilidade_details), name='get_habilidade_details'),
        path('buscar-habilidades/', self.admin_site.admin_view(self.buscar_habilidades), name='buscar_habilidades'),
    ]
    return custom_urls + urls

def buscar_habilidades(self, request):
    """Endpoint para buscar habilidades baseado no termo de busca."""
    if not request.user.is_staff:
        raise PermissionDenied
        
    term = request.GET.get('term', '')
    print(f'Termo de busca recebido: {term}')
    
    try:
        # Implementação da busca...
        return JsonResponse({'results': results})
    except Exception as e:
        print(f'Erro ao buscar habilidades: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)
```

## Como Funciona o Campo "Buscar Habilidade"

O campo "Buscar Habilidade" utiliza a biblioteca Select2 para criar uma interface de busca avançada. O fluxo de funcionamento é o seguinte:

1. O usuário digita um termo de busca no campo
2. O JavaScript faz uma requisição AJAX para o endpoint `/dashboard/admin/adaptacao_curricular/adaptacaocurricularindividualizada/buscar-habilidades/`
3. O método `buscar_habilidades` no `admin.py` processa a requisição e retorna os resultados em formato JSON
4. O Select2 exibe os resultados para o usuário selecionar

## Princípios Gerais para Correção de Problemas Similares

Para corrigir problemas similares em outros campos de busca do sistema, siga estes princípios:

1. **Verifique as URLs**: Certifique-se de que as URLs usadas nos arquivos JavaScript estejam corretas e incluam todos os segmentos necessários.

2. **Verifique os endpoints no admin.py**: Garanta que os métodos que respondem às requisições AJAX estejam corretamente implementados e registrados em `get_urls`.

3. **Teste as requisições AJAX**: Use o console do navegador para verificar se as requisições AJAX estão sendo feitas corretamente e se estão recebendo respostas válidas.

4. **Verifique a configuração do Select2**: Certifique-se de que o Select2 esteja corretamente configurado para processar as respostas do servidor.

## Aplicando em Outros Campos de Busca

Para aplicar estas correções em outros campos de busca com problemas similares:

1. Identifique o arquivo JavaScript que controla o campo
2. Verifique a URL usada para fazer as requisições AJAX
3. Corrija a URL para apontar para o endpoint correto
4. Verifique se o endpoint está corretamente implementado no arquivo `admin.py`
5. Teste o campo para garantir que a busca funcione corretamente

Seguindo estes passos, você poderá corrigir problemas similares em outros campos de busca do sistema.
