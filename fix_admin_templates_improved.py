#!/usr/bin/env python
import os
import re
import sys
import shutil
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

def backup_file(file_path):
    """Cria um backup do arquivo antes de modificá-lo"""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backup criado: {backup_path}")

def update_template_in_file(file_path):
    """Atualiza o template no arquivo admin.py"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Verifica se o arquivo usa o template incorreto
    if 'change_list_template = "admin/change_list_material_dashboard_base.html"' in content:
        # Substitui o template incorreto pelo template padrão do Django
        modified_content = content.replace(
            'change_list_template = "admin/change_list_material_dashboard_base.html"',
            ''  # Remove a linha completamente
        )
        
        # Também substitui o template antigo se estiver presente
        modified_content = modified_content.replace(
            'change_list_template = "admin/change_list_base.html"',
            ''  # Remove a linha completamente
        )
        
        # Verifica se houve alteração
        if content == modified_content:
            print(f"Nenhuma alteração necessária em {file_path}")
            return False
        
        # Faz backup do arquivo original
        backup_file(file_path)
        
        # Salva o conteúdo modificado
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print(f"Template atualizado em {file_path}")
        return True
    else:
        print(f"Arquivo {file_path} não usa o template incorreto.")
        return False

def find_admin_files():
    """Encontra todos os arquivos admin.py no projeto"""
    admin_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Ignora diretórios de ambiente virtual e migrações
        if 'venv' in root or 'migrations' in root or '.git' in root:
            continue
        
        if 'admin.py' in files:
            admin_files.append(os.path.join(root, 'admin.py'))
    
    return admin_files

def main():
    """Função principal"""
    admin_files = find_admin_files()
    print(f"Encontrados {len(admin_files)} arquivos admin.py")
    
    updated_count = 0
    for file_path in admin_files:
        if update_template_in_file(file_path):
            updated_count += 1
    
    print(f"\nProcesso concluído. {updated_count} arquivos foram atualizados.")

if __name__ == "__main__":
    main()
