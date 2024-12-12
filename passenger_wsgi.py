import os
import sys

# Adicione o caminho para o projeto
sys.path.insert(0, '/home/netsarim/spia')

# Adicione o caminho para o ambiente virtual (se aplicável)
# sys.path.insert(0, '/home/netsarim/virtualenv/spia/3.11/lib/python3.11/site-packages')

# Carregue a aplicação Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pia_config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()