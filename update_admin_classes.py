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
            model_admin_classes = re.findall(r'class\s+(\w+)\(.*ModelAdmin.*\):', content)
            
            if model_admin_classes:
                print(f"  Encontradas {len(model_admin_classes)} classes ModelAdmin:")
                for class_name in model_admin_classes:
                    print(f"    - {class_name}")
                    
                    # Verifica se a classe já tem um change_list_template definido
                    pattern = rf'class\s+{class_name}\(.*ModelAdmin.*\):(?:\s*[^\n]*\n)+?(?:\s*change_list_template\s*=\s*[\'"][^\'"]*[\'"])?'
                    match = re.search(pattern, content)
                    
                    if match:
                        class_def = match.group(0)
                        
                        if 'change_list_template' in class_def:
                            # Substitui o template existente
                            new_class_def = re.sub(
                                r'change_list_template\s*=\s*[\'"][^\'"]*[\'"]',
                                'change_list_template = "admin/change_list_base.html"',
                                class_def
                            )
                        else:
                            # Adiciona a configuração do template
                            indent = re.search(r'^(\s+)', class_def.split('\n')[1]).group(1) if '\n' in class_def else '    '
                            new_class_def = class_def + f"\n{indent}change_list_template = \"admin/change_list_base.html\""
                        
                        # Atualiza o conteúdo
                        content = content.replace(class_def, new_class_def)
                
                # Salva as alterações
                with open(admin_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Arquivo atualizado: {os.path.relpath(admin_file, base_path)}")
    
    print("\nAtualização concluída com sucesso!")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    update_admin_classes()
