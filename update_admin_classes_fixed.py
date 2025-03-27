#!/usr/bin/env python
import os
import re
import glob

def update_admin_classes():
    """
    Atualiza as classes ModelAdmin em todos os arquivos admin.py para usar o template
    change_list_base.html, mantendo o estilo do Material Dashboard 3 em todas as páginas.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Encontra todos os arquivos admin.py
    admin_files = glob.glob(
        os.path.join(base_path, '**', 'admin.py'),
        recursive=True
    )
    
    print(f"Encontrados {len(admin_files)} arquivos admin.py para atualizar.")
    
    # Para cada arquivo admin.py, adiciona a configuração do template
    for admin_file in admin_files:
        # Ignora arquivos em diretórios venv ou migrations
        if 'venv' in admin_file or 'migrations' in admin_file:
            continue
            
        print(f"Analisando: {os.path.relpath(admin_file, base_path)}")
        
        # Lê o conteúdo do arquivo
        with open(admin_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se o arquivo contém classes ModelAdmin
        if 'ModelAdmin' in content:
            # Cria uma cópia de backup
            backup_file = admin_file + '.bak'
            if not os.path.exists(backup_file):
                print(f"  Criando backup: {os.path.relpath(backup_file, base_path)}")
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Encontra todas as classes que herdam de ModelAdmin
            model_admin_pattern = r'class\s+(\w+)\((?:.*?)ModelAdmin(?:.*?)\):'
            model_admin_classes = re.findall(model_admin_pattern, content, re.DOTALL)
            
            if model_admin_classes:
                print(f"  Encontradas {len(model_admin_classes)} classes ModelAdmin:")
                
                # Divide o conteúdo em linhas para processamento mais seguro
                lines = content.split('\n')
                modified_lines = []
                
                i = 0
                while i < len(lines):
                    line = lines[i]
                    modified_lines.append(line)
                    
                    # Verifica se esta linha contém a definição de uma classe ModelAdmin
                    class_match = re.search(model_admin_pattern, line)
                    if class_match:
                        class_name = class_match.group(1)
                        print(f"    - {class_name}")
                        
                        # Avança para encontrar onde adicionar o template
                        j = i + 1
                        has_template = False
                        
                        # Procura pelo final da definição da classe ou pela configuração existente
                        while j < len(lines) and not re.match(r'^\s*class\s+', lines[j]):
                            if re.search(r'^\s*change_list_template\s*=', lines[j]):
                                # Substitui a configuração existente
                                modified_lines.append('    change_list_template = "admin/change_list_base.html"')
                                has_template = True
                                j += 1
                                break
                            modified_lines.append(lines[j])
                            j += 1
                        
                        # Se não encontrou a configuração, adiciona após a definição da classe
                        if not has_template:
                            # Determina a indentação apropriada
                            indent = '    '
                            if j > i + 1 and lines[i+1].startswith(' '):
                                indent_match = re.match(r'^(\s+)', lines[i+1])
                                if indent_match:
                                    indent = indent_match.group(1)
                            
                            # Adiciona a configuração do template
                            modified_lines.append(f"{indent}change_list_template = \"admin/change_list_base.html\"")
                        
                        i = j - 1  # Ajusta o índice para continuar a partir da última linha processada
                    
                    i += 1
                
                # Salva as alterações
                with open(admin_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(modified_lines))
                print(f"  Arquivo atualizado: {os.path.relpath(admin_file, base_path)}")
    
    print("\nAtualização concluída com sucesso!")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    update_admin_classes()
