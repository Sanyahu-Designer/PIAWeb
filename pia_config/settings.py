from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
if os.getenv('ENVIRONMENT', 'development') == 'production':
    BASE_DIR = Path('/home/netsarim/caraapiaweb')
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

ALLOWED_HOSTS = []
if ENVIRONMENT == 'development':
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '*'])
else:
    ALLOWED_HOSTS.extend(['caraa.piaweb.com.br', 'www.caraa.piaweb.com.br'])

# CSRF Settings
CSRF_TRUSTED_ORIGINS = []
if ENVIRONMENT == 'development':
    CSRF_TRUSTED_ORIGINS.extend([
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://pia.sanyahudesigner.com.br',
        'https://pia.sanyahudesigner.com.br'
    ])
else:
    CSRF_TRUSTED_ORIGINS.extend([
        'http://caraa.piaweb.com.br',
        'https://caraa.piaweb.com.br',
        'http://www.caraa.piaweb.com.br',
        'https://www.caraa.piaweb.com.br'
    ])

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
    'channels',
    'pia_config',
    'core',
    'profissionais_app',
    'escola',
    'neurodivergentes',
    'adaptacao_curricular',
    'django_ckeditor_5',
    'realtime',
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
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'pia_config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'pia_config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('PROD_DB_NAME' if ENVIRONMENT == 'production' else 'DEV_DB_NAME'),
        'USER': os.getenv('PROD_DB_USER' if ENVIRONMENT == 'production' else 'DEV_DB_USER'),
        'PASSWORD': os.getenv('PROD_DB_PASSWORD' if ENVIRONMENT == 'production' else 'DEV_DB_PASSWORD'),
        'HOST': os.getenv('PROD_DB_HOST' if ENVIRONMENT == 'production' else 'DEV_DB_HOST'),
        'PORT': os.getenv('PROD_DB_PORT' if ENVIRONMENT == 'production' else 'DEV_DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
            'raise_on_warnings': True,
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
    STATIC_ROOT = '/home/netsarim/caraa.piaweb.com.br/static'
    MEDIA_ROOT = '/home/netsarim/caraa.piaweb.com.br/media'

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
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "PIA Admin",
    "site_header": "PIA",
    "site_brand": "PIA",
    "site_logo": "pia_config/images/logo.webp",
    "login_logo": "pia_config/images/logo.webp",
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bem-vindo ao PIA",
    "copyright": "PIA - Plano Individual de Aprendizagem",
    "search_model": ["auth.User", "neurodivergentes.Neurodivergente"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Mensagens", "url": "realtime:chat_list"},
    ],
    "usermenu_links": [
        {"name": "Mensagens", "url": "realtime:chat_list", "icon": "fas fa-comments"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "neurodivergentes", "escola", "profissionais_app"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "neurodivergentes.Neurodivergente": "fas fa-user-graduate",
        "escola.Escola": "fas fa-school",
        "profissionais_app.Profissional": "fas fa-user-md",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
    "language_chooser": False,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [],
    "custom_links_in_field_set_template": False,
    "show_ui_builder": False,
    "topmenu_links": [],
    "usermenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [],
    "app_list_custom_labels": {
        "adaptacao_curricular": "Adaptação Curricular"
    },
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
        {"name": "", "url": "#", "icon": "fas fa-bell position-relative", "classes": "notification-icon"},
    ],
    
    "usermenu_links": [
        {"name": "Notificações", "url": "#", "icon": "fas fa-bell position-relative"},
        {"name": "Suporte", "url": "https://sanyahudesigner.com.br", "new_window": True, "icon": "fas fa-headset"},
    ],
    
    "navigation_expanded": False,
    "show_ui_builder": False,
    
    "show_footer": True,
    "footer_text": "Direitos Reservados 2023 PIA - Plano Individual de Aprendizagem - Desenvolvido por 46.815.218/0001-03",
    "footer_version": False,
    "footer_style": "text-align: center; font-size: 14px;",
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark bg-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "custom_css": None,
    "custom_js": None,
}