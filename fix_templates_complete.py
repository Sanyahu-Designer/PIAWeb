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

def get_app_name_from_path(file_path):
    """Extrai o nome da aplicação a partir do caminho do arquivo"""
    parts = file_path.split(os.sep)
    # O nome da aplicação é o diretório que contém o arquivo admin.py
    app_name = parts[-2]
    return app_name

def update_template_in_file(file_path):
    """Atualiza o template no arquivo admin.py para usar o template específico da aplicação"""
    app_name = get_app_name_from_path(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Padrão para encontrar classes ModelAdmin
    model_admin_pattern = r'class\s+(\w+Admin)\(.*\):'
    model_admin_classes = re.findall(model_admin_pattern, content)
    
    if not model_admin_classes:
        print(f"Nenhuma classe ModelAdmin encontrada em {file_path}")
        return False
    
    modified_content = content
    made_changes = False
    
    for admin_class in model_admin_classes:
        # Extrai o nome do modelo a partir do nome da classe Admin (remove 'Admin' do final)
        model_name = admin_class[:-5].lower() if admin_class.endswith('Admin') else admin_class.lower()
        
        # Verifica se já existe uma definição de change_list_template
        change_list_pattern = rf'class\s+{admin_class}\(.*\):\s*(?:[^\n]*\n\s+[^\n]*)*?\s+change_list_template\s*='
        
        if re.search(change_list_pattern, modified_content):
            # Substitui o template existente pelo template específico da aplicação
            modified_content = re.sub(
                r'(class\s+' + admin_class + r'\(.*\):\s*(?:[^\n]*\n\s+[^\n]*)*?\s+)change_list_template\s*=\s*["\'].*["\']',
                r'\1change_list_template = "admin/change_list.html"',
                modified_content
            )
            made_changes = True
        else:
            # Adiciona a definição de change_list_template se não existir
            modified_content = re.sub(
                r'(class\s+' + admin_class + r'\(.*\):)',
                r'\1\n    change_list_template = "admin/change_list.html"',
                modified_content
            )
            made_changes = True
    
    # Verifica se houve alteração
    if not made_changes:
        print(f"Nenhuma alteração necessária em {file_path}")
        return False
    
    # Faz backup do arquivo original
    backup_file(file_path)
    
    # Salva o conteúdo modificado
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    
    print(f"Template atualizado em {file_path}")
    return True

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

def ensure_change_list_template_exists():
    """Verifica se o template change_list.html existe e cria se necessário"""
    template_dir = os.path.join(BASE_DIR, 'templates', 'admin')
    template_path = os.path.join(template_dir, 'change_list.html')
    
    if not os.path.exists(template_path):
        os.makedirs(template_dir, exist_ok=True)
        
        # Conteúdo do template change_list.html
        template_content = """{% extends "admin/change_list_material_dashboard_base.html" %}
{% load i18n admin_urls static admin_list %}

{# Este template estende o template base do Material Dashboard 3 #}
"""
        
        with open(template_path, 'w', encoding='utf-8') as file:
            file.write(template_content)
        
        print(f"Template change_list.html criado em {template_path}")

def main():
    """Função principal"""
    # Garante que o template change_list.html existe
    ensure_change_list_template_exists()
    
    admin_files = find_admin_files()
    print(f"Encontrados {len(admin_files)} arquivos admin.py")
    
    updated_count = 0
    for file_path in admin_files:
        if update_template_in_file(file_path):
            updated_count += 1
    
    print(f"\nProcesso concluído. {updated_count} arquivos foram atualizados.")

if __name__ == "__main__":
    main()
