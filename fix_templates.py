#!/usr/bin/env python
import os
import glob
import re

def fix_templates():
    """
    Corrige os templates que foram atualizados para garantir que todos os blocos
    tenham tags de fechamento correspondentes.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(base_path, 'templates', 'admin')
    
    # Encontra todos os templates change_list_material_dashboard.html
    template_paths = glob.glob(
        os.path.join(templates_path, '**', 'change_list_material_dashboard.html'),
        recursive=True
    )
    
    print(f"Encontrados {len(template_paths)} templates para corrigir.")
    
    # Para cada template, verifica e corrige os blocos não fechados
    for template_path in template_paths:
        print(f"Verificando: {os.path.relpath(template_path, base_path)}")
        
        # Lê o conteúdo do template atual
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se há blocos não fechados
        modified = False
        
        # Corrige o bloco result_list
        if '{% block result_list %}' in content and '{% endblock result_list %}' not in content:
            # Substitui o fechamento da div table-responsive após a tabela
            content = re.sub(
                r'</table>\s*</div>\s*',
                '</table>\n              </div>\n            {% endblock result_list %}\n            ',
                content
            )
            modified = True
        
        # Verifica outros blocos que podem estar sem fechamento
        for block_name in ['content', 'pagination', 'object-tools']:
            if f'{{% block {block_name} %}}' in content and f'{{% endblock {block_name} %}}' not in content:
                if block_name == 'content' and '{% endblock %}' in content:
                    # Se há um endblock genérico, substitui pelo específico
                    content = content.replace('{% endblock %}', f'{{% endblock {block_name} %}}')
                    modified = True
                else:
                    print(f"  Aviso: Bloco '{block_name}' não fechado em {os.path.relpath(template_path, base_path)}")
        
        # Salva as alterações se o conteúdo foi modificado
        if modified:
            print(f"  Corrigindo blocos não fechados em {os.path.relpath(template_path, base_path)}")
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print("\nCorreção concluída com sucesso!")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    fix_templates()
