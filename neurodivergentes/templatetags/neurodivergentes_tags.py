from django import template
import json

register = template.Library()

@register.filter
def get_item(value, key):
    """
    Função flexível para acessar itens em dicionários ou listas de dicionários
    """
    if isinstance(value, dict):
        return value.get(key, '-')
    
    if isinstance(value, list):
        # Procura na lista de dicionários pelo item com 'pdi_data' correspondente
        for item in value:
            if item.get('pdi_data') == key:
                return item.get('progresso', '-')
    
    return '-'

@register.filter
def jsonify(obj):
    """
    Template filter to convert an object to JSON.
    Usage: {{ object|jsonify }}
    """
    return json.dumps(obj)
