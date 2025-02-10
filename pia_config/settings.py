from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-l#65p7z-m9f4n-v02tgnf9rm%4!=u@fke*g4)brw$8+ym-$szj'

DEBUG = True

ALLOWED_HOSTS = ['pia.sanyahudesigner.com.br', '*', 'localhost']  # Ajuste para seu domínio

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://pia.sanyahudesigner.com.br',
    'https://pia.sanyahudesigner.com.br'
]

# Duração padrão da sessão (2 semanas)
SESSION_COOKIE_AGE = 1209600  # em segundos

# Define se a sessão expira ao fechar o navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pia_config',
    'core',
    'profissionais_app',
    'escola',
    'neurodivergentes',
    'ckeditor',
]

LOGIN_REDIRECT_URL = '/admin/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# CKEditor settings
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['NumberedList', 'BulletedList'],
            ['Undo', 'Redo'],
        ],
        'height': 300,
        'width': '100%',
        'removePlugins': 'elementspath,resize',
        'toolbarCanCollapse': False,
        'contentsCss': ['body { margin: 10px; }'],
        'enterMode': 2,  # CKEDITOR.ENTER_BR
        'shiftEnterMode': 1,  # CKEDITOR.ENTER_P
        'extraPlugins': 'autogrow',
        'autoGrow_minHeight': 300,
        'autoGrow_maxHeight': 600,
    },
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
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'pia_config.urls'

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'pia_config/templates'),
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'neurodivergentes/templates/neurodivergentes'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'pia_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_520_ci',
        }
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
import os
from pathlib import Path

# Configuração do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuração de URLs estáticas
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "profissionais_app/static",
    BASE_DIR / "escola/static",
    BASE_DIR / "neurodivergentes/static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configurações de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuração para servir arquivos de mídia em produção
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "LANG": "pt-BR",
    "show_ui_language_toggle": False,
    "site_title": "PIA | Dashboard",
    "site_header": "PIA | Dashboard",
    "site_brand": "PIA | Dashboard",
    "site_logo": "pia_config/images/logo.webp",
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "",
    "site_icon": "pia_config/images/logo.webp",
    "welcome_sign": "Seja Bem vindo ao PIA - Plano Individual de Aprendizagem",
    "copyright": "PIA - Plano Individual de Aprendizagem - Desenvolvido por 46.815.218/0001-03",
    "user_avatar": None,
    "search_model": ["auth.User"],
        
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ajuda", "url": "https://sanyahudesigner.com.br", "new_window": True},
    ],
    
    "usermenu_links": [
        {"name": "Suporte", "url": "https://sanyahudesigner.com.br", "new_window": True, 'icon': 'fas fa-headset'},
    ],
    
    "navigation_expanded": False,
    "show_ui_builder": False,
    
    "show_footer": True,
    "footer_text": "Direitos Reservados © {% now 'Y' %} PIA - Plano Individual de Aprendizagem - Desenvolvido por 46.815.218/0001-03",
    "footer_version": False,
    "footer_style": "text-align: center; font-size: 14px;",
}