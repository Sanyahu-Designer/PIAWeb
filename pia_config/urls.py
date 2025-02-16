from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', admin.site.urls),
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
]

# Servir arquivos de mídia em produção
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        # Rota específica para servir arquivos de mídia em produção
        path('media/<path:path>', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]