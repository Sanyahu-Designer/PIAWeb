from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'neurodivergentes'

urlpatterns = [
    path('pdi/<int:pdi_id>/popup/', views.pdi_popup_view, name='pdi_popup_view'),
    path('relatorio/<int:neurodivergente_id>/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('grafico/<int:neurodivergente_id>/', views.grafico_evolucao, name='grafico_evolucao'),
    path('api/condicoes/', views.get_condicoes, name='get_condicoes'),
    path('pdi/<int:pdi_id>/imprimir/', views.imprimir_pdi, name='imprimir_pdi'),
    path('aluno/<int:aluno_id>/pdis/imprimir/', views.imprimir_pdis_aluno, name='imprimir_pdis_aluno'),
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)