#!/usr/bin/env python
import os
import shutil
import glob

def restore_backups():
    """
    Restaura os backups dos templates que foram modificados para corrigir os erros de sintaxe.
    """
    # Caminho base do projeto
    base_path = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(base_path, 'templates', 'admin')
    
    # Encontra todos os arquivos de backup .bak
    backup_paths = glob.glob(
        os.path.join(templates_path, '**', '*.bak'),
        recursive=True
    )
    
    print(f"Encontrados {len(backup_paths)} arquivos de backup para restaurar.")
    
    # Para cada backup, restaura o arquivo original
    for backup_path in backup_paths:
        original_path = backup_path[:-4]  # Remove a extensão .bak
        print(f"Restaurando: {os.path.relpath(original_path, base_path)}")
        
        # Restaura o backup
        shutil.copy2(backup_path, original_path)
        
        # Remove o arquivo de backup
        os.remove(backup_path)
    
    print("\nRestauração concluída com sucesso!")
    print("Por favor, reinicie o servidor para ver as mudanças.")

if __name__ == "__main__":
    restore_backups()
