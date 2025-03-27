#!/usr/bin/env python
import os
import re
import sys
import shutil
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent

# Mapeamento de aplicações para templates específicos
APP_TEMPLATE_MAPPING = {
    'neurodivergentes/admin.py': 'admin/neurodivergentes/neurodivergente/change_list_material_dashboard.html',
    'adaptacao_curricular/admin.py': 'admin/adaptacao_curricular/adaptacaocurricularindividualizada/change_list_material_dashboard.html',
    'escola/admin.py': 'admin/escola/escola/change_list_material_dashboard.html',
    'profissionais_app/admin.py': 'admin/profissionais_app/profissional/change_list_material_dashboard.html',
    'pia_config/admin.py': 'admin/auth/user/change_list_material_dashboard.html',
    # Adicione mais mapeamentos conforme necessário
}

def backup_file(file_path):
    """Cria um backup do arquivo antes de modificá-lo"""
    backup_path = f"{file_path}.bak"
    shutil.copy2(file_path, backup_path)
    print(f"Backup criado: {backup_path}")

def update_template_in_file(file_path, template_path):
    """Atualiza o template no arquivo admin.py para usar o template específico"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Substitui o template genérico pelo específico
    modified_content = re.sub(
        r'change_list_template\s*=\s*"admin/change_list_material_dashboard_base\.html"',
        f'change_list_template = "{template_path}"',
        content
    )
    
    # Também substitui o template antigo se estiver presente
    modified_content = re.sub(
        r'change_list_template\s*=\s*"admin/change_list_base\.html"',
        f'change_list_template = "{template_path}"',
        content
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
    
    print(f"Template atualizado em {file_path} para usar {template_path}")
    return True

def main():
    """Função principal"""
    updated_count = 0
    
    for app_path, template_path in APP_TEMPLATE_MAPPING.items():
        file_path = os.path.join(BASE_DIR, app_path)
        if os.path.exists(file_path):
            if update_template_in_file(file_path, template_path):
                updated_count += 1
        else:
            print(f"Arquivo não encontrado: {file_path}")
    
    print(f"\nProcesso concluído. {updated_count} arquivos foram atualizados.")

if __name__ == "__main__":
    main()
