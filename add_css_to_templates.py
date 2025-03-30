#!/usr/bin/env python3

import os
import re
import sys

# Diretório base dos templates
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'admin')

# Padrão para encontrar o bloco extrastyle
EXTRASTYLE_PATTERN = r'({% block extrastyle %}{{ block.super }})'  # Grupo 1: início do bloco

# Linha CSS a ser adicionada
CSS_LINE = '<link rel="stylesheet" type="text/css" href="{% static \'admin/css/form_fields_style.css\' %}">'  # Linha a ser adicionada

# Lista de templates a serem ignorados (caminhos completos)
IGNORE_PATHS = [
    os.path.join(TEMPLATES_DIR, 'change_form_material.html'),  # Template base
    os.path.join(TEMPLATES_DIR, 'change_form.html'),          # Template base
    os.path.join(TEMPLATES_DIR, 'neurodivergentes', 'neurodivergente', 'change_form.html'),  # Já está correto
    os.path.join(TEMPLATES_DIR, 'adaptacao_curricular', 'adaptacaocurricularindividualizada', 'change_form.html')  # Não funcionou bem
]

# Função para encontrar todos os templates de cadastro
def find_change_form_templates(base_dir):
    templates = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == 'change_form.html':
                full_path = os.path.join(root, file)
                if full_path not in IGNORE_PATHS:
                    templates.append(full_path)
    return templates

# Função para verificar se o CSS já está incluído no template
def css_already_included(content):
    return 'form_fields_style.css' in content

# Função para adicionar a linha CSS ao bloco extrastyle
def add_css_to_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Verifica se o CSS já está incluído
    if css_already_included(content):
        print(f"[Já incluído] {os.path.relpath(template_path, TEMPLATES_DIR)}")
        return False
    
    # Verifica se o template estende outro template
    extends_match = re.search(r'{% extends ["\'](.+?)["\'] %}', content)
    if not extends_match:
        print(f"[Erro] {os.path.relpath(template_path, TEMPLATES_DIR)} não estende nenhum template")
        return False
    
    # Verifica se o bloco extrastyle existe
    extrastyle_match = re.search(EXTRASTYLE_PATTERN, content)
    if not extrastyle_match:
        # Se não existir, adiciona o bloco completo após a linha de extends
        extends_line = extends_match.group(0)
        new_block = f'''
{{% load i18n admin_urls static %}}  {{# Garante que static está carregado #}}

{{% block extrastyle %}}{{{{{ block.super }}}}}
{CSS_LINE}
{{% endblock %}}
'''
        content = content.replace(extends_line, extends_line + new_block)
    else:
        # Se existir, adiciona a linha CSS após o início do bloco
        start = extrastyle_match.group(1)
        content = content.replace(start, f"{start}\n{CSS_LINE}")
    
    # Salva o template modificado
    with open(template_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"[Modificado] {os.path.relpath(template_path, TEMPLATES_DIR)}")
    return True

# Função principal
def main():
    print("Iniciando a adição do CSS aos templates de cadastro...\n")
    
    # Encontra todos os templates de cadastro
    templates = find_change_form_templates(TEMPLATES_DIR)
    
    if not templates:
        print("Nenhum template de cadastro encontrado!")
        return
    
    print(f"Encontrados {len(templates)} templates de cadastro.\n")
    print("Templates a serem processados:")
    for template in templates:
        print(f"- {os.path.relpath(template, TEMPLATES_DIR)}")
    print()
    
    # Confirma com o usuário antes de prosseguir
    confirm = input("Deseja prosseguir com a modificação? (s/n): ").lower()
    if confirm != 's':
        print("Operação cancelada pelo usuário.")
        return
    
    # Adiciona o CSS a cada template
    modified = 0
    for template in templates:
        if add_css_to_template(template):
            modified += 1
    
    print(f"\nProcesso concluído! {modified} templates foram modificados.")

if __name__ == "__main__":
    main()
