from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Importante: a ordem das URLs importa!
# Colocamos as URLs do realtime antes das URLs do admin
# para garantir que nossas URLs personalizadas tenham precedência
urlpatterns = [
    # URLs do realtime (devem vir antes do admin)
    path('dashboard/realtime/', include('realtime.urls', namespace='realtime')),
    
    # URLs do admin
    path('dashboard/', admin.site.urls),
    
    # Outras URLs
    path('', CustomLoginView.as_view(
        template_name='pia_config/login.html',
        next_page='/dashboard/'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='logout'),
    path('escolas/', include('escola.urls')),
    path('profissionais/', include('profissionais_app.urls')),
    path('neurodivergentes/', include('neurodivergentes.urls')),
    path('adaptacao-curricular/', include('adaptacao_curricular.urls')),
    
    # Adicionar uma URL para a página de teste de WebSocket
    path('websocket-test/', lambda request: serve(request, 'websocket-test.html', document_root=settings.STATIC_ROOT)),
]

# Servir arquivos estáticos e de mídia
# Isso é necessário para o Daphne servir arquivos estáticos
urlpatterns += [
    # Rota para servir arquivos estáticos
    path('static/<path:path>', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
    
    # Rota para servir arquivos de mídia
    path('media/<path:path>', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# Adicionar as rotas padrão do Django para arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)