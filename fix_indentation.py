#!/usr/bin/env python
import os
import re
import glob

def fix_indentation():
    """
    Corrige problemas de indentação nos arquivos admin.py que foram modificados.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Encontra todos os arquivos admin.py
    admin_files = glob.glob(
        os.path.join(base_path, '**', 'admin.py'),
        recursive=True
    )
    
    print(f"Verificando {len(admin_files)} arquivos admin.py para corrigir indentação.")
    
    # Para cada arquivo admin.py, verifica e corrige problemas de indentação
    for admin_file in admin_files:
        # Ignora arquivos em diretórios venv ou migrations
        if 'venv' in admin_file or 'migrations' in admin_file:
            continue
            
        print(f"Verificando: {os.path.relpath(admin_file, base_path)}")
        
        # Lê o conteúdo do arquivo
        with open(admin_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Verifica se há problemas de indentação
        modified = False
        for i, line in enumerate(lines):
            # Procura por linhas com 'change_list_template' que possam ter indentação incorreta
            if 'change_list_template' in line:
                # Verifica se a linha anterior é a definição de uma classe
                if i > 0 and 'class' in lines[i-1] and ':' in lines[i-1]:
                    # Corrige a indentação para 4 espaços
                    lines[i] = '    change_list_template = "admin/change_list_base.html"\n'
                    modified = True
                    print(f"  Corrigida indentação na linha {i+1}")
                # Verifica se a linha está dentro de uma classe (indentada)
                elif i > 0 and not lines[i].startswith('    '):
                    # Procura pela indentação da linha anterior
                    prev_indent = re.match(r'^(\s+)', lines[i-1])
                    if prev_indent:
                        # Usa a mesma indentação da linha anterior
                        lines[i] = prev_indent.group(1) + 'change_list_template = "admin/change_list_base.html"\n'
                    else:
                        # Usa 4 espaços como padrão
                        lines[i] = '    change_list_template = "admin/change_list_base.html"\n'
                    modified = True
                    print(f"  Corrigida indentação na linha {i+1}")
        
        # Se houve modificações, salva o arquivo
        if modified:
            with open(admin_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f"  Arquivo atualizado: {os.path.relpath(admin_file, base_path)}")
    
    print("\nCorreção de indentação concluída!")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    fix_indentation()
