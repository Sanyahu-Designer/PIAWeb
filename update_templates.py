#!/usr/bin/env python
import os
import shutil
import glob
import re

def update_templates():
    """
    Atualiza todos os templates change_list_material_dashboard.html para usar o mesmo estilo
    da página modelo de Alunos/Pacientes, mantendo as especificidades de cada modelo.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(base_path, 'templates', 'admin')
    
    # Caminho do template modelo (Alunos/Pacientes)
    model_template_path = os.path.join(
        templates_path, 'neurodivergentes', 'neurodivergente', 
        'change_list_material_dashboard.html'
    )
    
    # Caminho do template base para listas
    base_template_path = os.path.join(
        templates_path, 'change_list', 'change_list_material_dashboard_base.html'
    )
    
    # Garante que o diretório do template base existe
    os.makedirs(os.path.dirname(base_template_path), exist_ok=True)
    
    # Lê o conteúdo do template modelo
    with open(model_template_path, 'r', encoding='utf-8') as f:
        model_content = f.read()
    
    # Encontra todos os templates change_list_material_dashboard.html
    template_paths = glob.glob(
        os.path.join(templates_path, '**', 'change_list_material_dashboard.html'),
        recursive=True
    )
    
    # Exclui o template modelo e o template base da lista de atualização
    template_paths = [p for p in template_paths 
                     if p != model_template_path and p != base_template_path]
    
    print(f"Encontrados {len(template_paths)} templates para atualizar.")
    
    # Para cada template, atualiza mantendo as especificidades do modelo
    for template_path in template_paths:
        print(f"Atualizando: {os.path.relpath(template_path, base_path)}")
        
        # Lê o conteúdo do template atual
        with open(template_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Extrai o app_label e model_name do caminho do template
        path_parts = os.path.relpath(template_path, templates_path).split(os.sep)
        app_label = path_parts[0]
        model_name = path_parts[1] if len(path_parts) > 1 else None
        
        # Cria uma cópia de backup
        backup_path = template_path + '.bak'
        shutil.copy2(template_path, backup_path)
        
        # Substitui o conteúdo, mantendo as especificidades do modelo
        new_content = model_content
        
        # Ajusta o breadcrumb para o app e modelo específico
        if app_label and model_name:
            # Substitui o link para o app específico no breadcrumb
            new_content = re.sub(
                r'<li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="{% url \'admin:app_list\' app_label=\'neurodivergentes\' %}">Aluno/Paciente</a></li>',
                f'<li class="breadcrumb-item text-sm"><a class="opacity-5 text-dark" href="{{% url \'admin:app_list\' app_label=\'{app_label}\' %}}">{{{{ opts.app_config.verbose_name }}</a></li>',
                new_content
            )
            
            # Ajusta o placeholder de pesquisa
            new_content = re.sub(
                r'placeholder="Pesquisar Aluno/Paciente"',
                'placeholder="Pesquisar {{ cl.opts.verbose_name }}"',
                new_content
            )
        
        # Escreve o conteúdo atualizado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    print("\nAtualização concluída com sucesso!")
    print("Backups dos templates originais foram criados com a extensão .bak")

if __name__ == "__main__":
    update_templates()
