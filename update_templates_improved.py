#!/usr/bin/env python
import os
import shutil
import glob
import re

def update_templates():
    """
    Atualiza todos os templates change_list_material_dashboard.html para usar o mesmo estilo
    da página modelo de Alunos/Pacientes, mas preservando a estrutura de dados específica de cada modelo.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(base_path, 'templates', 'admin')
    
    # Encontra todos os templates change_list_material_dashboard.html
    template_paths = glob.glob(
        os.path.join(templates_path, '**', 'change_list_material_dashboard.html'),
        recursive=True
    )
    
    # Caminho do template modelo (Alunos/Pacientes)
    model_template_path = os.path.join(
        templates_path, 'neurodivergentes', 'neurodivergente', 
        'change_list_material_dashboard.html'
    )
    
    # Exclui o template modelo da lista de atualização
    template_paths = [p for p in template_paths if p != model_template_path]
    
    print(f"Encontrados {len(template_paths)} templates para atualizar.")
    
    # Lê o conteúdo do template modelo
    with open(model_template_path, 'r', encoding='utf-8') as f:
        model_content = f.read()
    
    # Extrai as partes do template modelo que queremos manter (estilo e estrutura geral)
    # Cabeçalho (extends, load, blocks de estilo)
    header_pattern = r'{% extends.*?{% block breadcrumbs %}.*?{% endblock %}'
    header_match = re.search(header_pattern, model_content, re.DOTALL)
    header_content = header_match.group(0) if header_match else ""
    
    # Início do bloco de conteúdo até a tabela
    content_start_pattern = r'{% block content %}.*?<div class="table-responsive p-0">'
    content_start_match = re.search(content_start_pattern, model_content, re.DOTALL)
    content_start = content_start_match.group(0) if content_start_match else ""
    
    # Final do bloco de conteúdo (após a tabela)
    content_end_pattern = r'{% endblock result_list %}.*?{% endblock %}'
    content_end_match = re.search(content_end_pattern, model_content, re.DOTALL)
    content_end = content_end_match.group(0) if content_end_match else ""
    
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
        
        # Extrai a parte específica do modelo (tabela com os dados)
        table_pattern = r'<table id="result_list".*?</table>'
        table_match = re.search(table_pattern, current_content, re.DOTALL)
        table_content = table_match.group(0) if table_match else ""
        
        if not table_content:
            # Se não encontrar a tabela, tenta extrair o bloco result_list inteiro
            result_list_pattern = r'{% block result_list %}.*?{% endblock result_list %}'
            result_list_match = re.search(result_list_pattern, current_content, re.DOTALL)
            result_list_content = result_list_match.group(0) if result_list_match else ""
            
            # Constrói o novo conteúdo
            new_content = header_content.replace("Aluno/Paciente", f"{{{{ opts.app_config.verbose_name }}}}")
            new_content = new_content.replace("{% url 'admin:app_list' app_label='neurodivergentes' %}", "{% url 'admin:app_list' app_label=opts.app_label %}")
            new_content += "\n{% block content %}\n<div class=\"container-fluid py-2\">\n  <div class=\"row\">\n    <div class=\"col-12\">\n      <div class=\"card my-4\">\n        <div class=\"card-header p-0 position-relative mt-n4 mx-3 z-index-2\">\n          <div class=\"shadow-dark border-radius-lg pt-4 pb-3\" style=\"background: linear-gradient(to right, #6c757d, #8d99ae);\">\n            <h6 class=\"text-white text-capitalize ps-3\">{{ cl.opts.verbose_name_plural|capfirst }}</h6>\n          </div>\n        </div>\n        <div class=\"card-body px-0 pb-2\">\n          <!-- Campo de Pesquisa Elegante -->\n          <div class=\"px-4 py-3\">\n            <form id=\"changelist-search\" method=\"get\" class=\"mb-0\">\n              <div class=\"d-flex align-items-center\">\n                <div class=\"input-group flex-grow-1\">\n                  <input type=\"text\" name=\"q\" value=\"{{ cl.query }}\" class=\"form-control\" id=\"searchbar\" placeholder=\"Pesquisar {{ cl.opts.verbose_name }}\">\n                </div>\n                <button type=\"submit\" class=\"btn btn-outline-primary btn-sm ms-2 mb-0 d-flex align-items-center justify-content-center\">\n                  <i class=\"material-symbols-rounded opacity-10\" style=\"font-size: 20px;\">search</i>\n                </button>\n              </div>\n              {% for pair in cl.params.items %}\n                {% if pair.0 != 'q' %}<input type=\"hidden\" name=\"{{ pair.0 }}\" value=\"{{ pair.1 }}\">{% endif %}\n              {% endfor %}\n            </form>\n          </div>\n          \n          {% if cl.formset and cl.formset.errors %}\n            <p class=\"errornote\">\n              {% blocktranslate count errors=cl.formset.total_error_count %}Please correct the error below.{% plural %}Please correct the errors below.{% endblocktranslate %}\n            </p>\n            {{ cl.formset.non_form_errors }}\n          {% endif %}\n          \n          <div class=\"changelist-form-container\">\n"
            new_content += result_list_content
            new_content += "\n            {% block pagination %}\n              {% if cl.result_count != cl.full_result_count %}\n                <div class=\"px-4 py-2\">\n                  <p class=\"text-sm text-secondary\">\n                    {% blocktranslate with cl.result_count as count and cl.full_result_count as full_count %}\n                      {{ count }} of {{ full_count }} selected\n                    {% endblocktranslate %}\n                  </p>\n                </div>\n              {% endif %}\n              \n              <div class=\"px-4 py-2 d-flex justify-content-center\">\n                {% pagination cl %}\n              </div>\n            {% endblock %}\n          </div>\n        </div>\n      </div>\n    </div>\n  </div>\n</div>\n{% endblock %}"
        else:
            # Constrói o novo conteúdo
            new_content = header_content.replace("Aluno/Paciente", f"{{{{ opts.app_config.verbose_name }}}}")
            new_content = new_content.replace("{% url 'admin:app_list' app_label='neurodivergentes' %}", "{% url 'admin:app_list' app_label=opts.app_label %}")
            new_content += content_start.replace("Pesquisar Aluno/Paciente", "Pesquisar {{ cl.opts.verbose_name }}")
            new_content += f"\n                {table_content}\n              "
            new_content += content_end
        
        # Escreve o conteúdo atualizado
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    print("\nAtualização concluída com sucesso!")
    print("Backups dos templates originais foram criados com a extensão .bak")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    update_templates()
