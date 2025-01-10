from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    pdi_popup_view,
    gerar_relatorio_pdf,
    gerar_relatorio_geral_html,
    grafico_evolucao,
    get_condicoes,
    imprimir_pdi,
    imprimir_pdis_aluno,
    teste_pdf_view
)

app_name = 'neurodivergentes'

urlpatterns = [
    path('pdi/<int:pdi_id>/popup/', pdi_popup_view, name='pdi_popup_view'),
    path('relatorio/<int:neurodivergente_id>/', gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('relatorio-geral-html/<int:neurodivergente_id>/', gerar_relatorio_geral_html, name='gerar_relatorio_geral_html'),
    path('grafico/<int:neurodivergente_id>/', grafico_evolucao, name='grafico_evolucao'),
    path('api/condicoes/', get_condicoes, name='get_condicoes'),
    path('pdi/<int:pdi_id>/imprimir/', imprimir_pdi, name='imprimir_pdi'),
    path('aluno/<int:aluno_id>/pdis/imprimir/', imprimir_pdis_aluno, name='imprimir_pdis_aluno'),
    path('teste-pdf/', teste_pdf_view, name='teste_pdf'),
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)