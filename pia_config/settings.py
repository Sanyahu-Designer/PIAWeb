from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
if os.getenv('ENVIRONMENT', 'development') == 'production':
    BASE_DIR = Path('/home/netsarim/app_piaweb')
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Ambiente de execução (development ou production)
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = ENVIRONMENT == 'development'

# Configurações de Segurança
if ENVIRONMENT == 'production':
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Gerar uma nova SECRET_KEY para produção
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-l#65p7z-m9f4n-v02tgnf9rm%4!=u@fke*g4)brw$8+ym-$szj')
else:
    SECRET_KEY = 'django-insecure-l#65p7z-m9f4n-v02tgnf9rm%4!=u@fke*g4)brw$8+ym-$szj'

# Chave exclusiva para criptografia de campos sensíveis
ENCRYPTED_MODEL_FIELDS_KEY = os.environ.get('ENCRYPTED_MODEL_FIELDS_KEY', SECRET_KEY)

# Chave obrigatória para django-encrypted-model-fields
FIELD_ENCRYPTION_KEY = os.environ.get('FIELD_ENCRYPTION_KEY', 'r0kEoE2kakZK8Ms8g-iRJexQVYCqO_X4FgPVmOior_Y=')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'app.piaweb.com.br',
    'www.app.piaweb.com.br',
]

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://app.piaweb.com.br',
    'https://www.app.piaweb.com.br',
]

# Duração padrão da sessão (2 semanas)
SESSION_COOKIE_AGE = 1209600  # em segundos

# Define se a sessão expira ao fechar o navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Application definition
INSTALLED_APPS = [
    'django_multitenant',
    'neurodivergentes',
    'django.contrib.admin',
    'django.contrib.auth',  # Mantendo a aplicação auth original
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'pia_config',
    'core',
    'profissionais_app',
    'escola',
    'adaptacao_curricular',
    'django_ckeditor_5',
    'realtime',
    'configuracoes',
    'institucional',
    'clientes',
    'usuarios',
]

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# CKEditor settings
# Django CKEditor 5 settings
CUSTOMIZE_CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['bold', 'italic', 'underline',
                   '|', 'bulletedList', 'numberedList',
                   '|', 'alignment',
                   '|', 'undo', 'redo'],
        'height': '300px',
        'width': '100%',
        'removePlugins': ['elementspath', 'resize'],
        'toolbar_Basic': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Undo', 'Redo'],
        ],
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'clientes.middleware.ImpersonationMiddleware',
    'clientes.tenant_middleware.TenantMiddleware',
    'pia_config.middleware.RedirectLoginMiddleware',  # Novo middleware para interceptar redirecionamentos para login
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'pia_config/templates'),
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'neurodivergentes/templates/neurodivergentes'),
            os.path.join(BASE_DIR, 'realtime/templates'),
            os.path.join(BASE_DIR, 'realtime/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'clientes.context_processors.superuser_permissions',
            ],
        },
    },
]

WSGI_APPLICATION = 'pia_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PROD_DB_NAME' if ENVIRONMENT == 'production' else 'DEV_DB_NAME'),
        'USER': os.getenv('PROD_DB_USER' if ENVIRONMENT == 'production' else 'DEV_DB_USER'),
        'PASSWORD': os.getenv('PROD_DB_PASSWORD' if ENVIRONMENT == 'production' else 'DEV_DB_PASSWORD'),
        'HOST': os.getenv('PROD_DB_HOST' if ENVIRONMENT == 'production' else 'DEV_DB_HOST'),
        'PORT': os.getenv('PROD_DB_PORT' if ENVIRONMENT == 'production' else 'DEV_DB_PORT'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale'
]

# Configurações de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Diretório principal de estáticos
    BASE_DIR / "neurodivergentes/static",
    BASE_DIR / "profissionais_app/static",
    BASE_DIR / "escola/static",
    BASE_DIR / "realtime/static",
]

if ENVIRONMENT == 'development':
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    STATIC_ROOT = '/home/netsarim/app.piaweb.com.br/static'
    MEDIA_ROOT = '/home/netsarim/app.piaweb.com.br/media'

# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

# CKEditor 5 settings (mantendo as mesmas funcionalidades do CKEditor 4)
CUSTOMIZE_CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['bold', 'italic', 'underline',
                   '|', 'bulletedList', 'numberedList',
                   '|', 'alignment',
                   '|', 'undo', 'redo'],
        'height': '300px',
        'width': '100%',
    }
}
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Channels Configuration
ASGI_APPLICATION = 'pia_config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    }
}

# Material Dashboard Settings
MATERIAL_DASHBOARD_SETTINGS = {
    "site_title": "PIA",
    "site_header": "PIA",
    "site_brand": "Painel PIA",
    "site_logo": "pia_config/images/logo.webp",
    "footer_text": "Direitos Reservados 2025 PIA - Plano Individual de Aprendizagem - Desenvolvido por 46.815.218/0001-03"
}

# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'audit': {
            'format': 'AUDIT {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/pia.log'),
            'formatter': 'verbose',
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/audit.log'),
            'formatter': 'audit',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'clientes': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'audit': {
            'handlers': ['audit_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Criar diretório de logs se não existir
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)