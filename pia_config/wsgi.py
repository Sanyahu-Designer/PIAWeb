"""
WSGI config for pia_config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pia_config.settings')

application = get_wsgi_application()



# QUANDO ESTIVER EM PRODUÇÃO HABILITAR O DE BAIXO E APAGAR O DE CIMA
# E ALTERAR O ENDEREÇO ROOT CASO PRECISE

## import os
## from django.core.wsgi import get_wsgi_application
## from whitenoise import WhiteNoise

## os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pia_config.settings')

## application = get_wsgi_application()
## application = WhiteNoise(application, root='/home/netsarim/spia/staticfiles')  # Verifique se o caminho está correto
