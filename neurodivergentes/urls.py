from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .graficos_parecer import dados_graficos_parecer
from .views import (
    lista_pei,
    pei_popup_view,
    imprimir_pei,
    gerar_relatorio_pei_pdf,
    pdi_popup_view,
    gerar_relatorio_pdf,
    gerar_relatorio_geral_html,
    grafico_evolucao,
    get_condicoes,
    imprimir_pdi,
    imprimir_pdis_aluno,
    teste_pdf_view,
    lista_evolucao,
    evolucao_popup_view,
    imprimir_evolucao,
    gerar_relatorio_evolucao_html,
    imprimir_parecer,
    gerar_relatorio_parecer_pdf,
    gerar_relatorio_parecer_geral_pdf,
    imprimir_anamnese
)
from .admin_views import ParecerGraficosView
from .graficos_parecer import dados_graficos_parecer


app_name = 'neurodivergentes'

urlpatterns = [
    path('parecer/<int:parecer_id>/imprimir/',
         imprimir_parecer,
         name='imprimir_parecer'),
    path('relatorio-parecer/<int:neurodivergente_id>/',
         gerar_relatorio_parecer_pdf,
         name='gerar_relatorio_parecer_pdf'),
    path('relatorio-parecer-geral-pdf/<int:neurodivergente_id>/',
         gerar_relatorio_parecer_geral_pdf,
         name='gerar_relatorio_parecer_geral_pdf'),
    path('parecer/<int:parecer_id>/graficos/', 
         ParecerGraficosView.as_view(), 
         name='parecer_graficos'),
    path('api/graficos-parecer/', dados_graficos_parecer, name='dados_graficos_parecer'),
    path('pdi/<int:pdi_id>/popup/', pdi_popup_view, name='pdi_popup_view'),
    path('relatorio/<int:neurodivergente_id>/', gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('relatorio-geral-html/<int:neurodivergente_id>/', gerar_relatorio_geral_html, name='gerar_relatorio_geral_html'),
    path('grafico/<int:neurodivergente_id>/', grafico_evolucao, name='grafico_evolucao'),
    path('api/condicoes/', get_condicoes, name='get_condicoes'),
    path('pdi/<int:pdi_id>/imprimir/', imprimir_pdi, name='imprimir_pdi'),
    path('aluno/<int:aluno_id>/pdis/imprimir/', imprimir_pdis_aluno, name='imprimir_pdis_aluno'),
    path('teste-pdf/', teste_pdf_view, name='teste_pdf'),
    path('aluno/<int:aluno_id>/evolucao/', lista_evolucao, name='lista_evolucao'),
    path('aluno/<int:aluno_id>/evolucao/<int:evolucao_id>/', lista_evolucao, name='visualizar_evolucao'),
    path('evolucao/<int:evolucao_id>/popup/', evolucao_popup_view, name='evolucao_popup'),
    path('evolucao/<int:evolucao_id>/imprimir/', imprimir_evolucao, name='imprimir_evolucao'),
    path('relatorio-evolucao-html/<int:neurodivergente_id>/', gerar_relatorio_evolucao_html, name='gerar_relatorio_evolucao_html'),
    # URLs do PEI
    path('aluno/<int:aluno_id>/pei/', lista_pei, name='lista_pei'),
    path('pei/<int:pei_id>/popup/', pei_popup_view, name='pei_popup'),
    path('pei/<int:pei_id>/imprimir/', imprimir_pei, name='imprimir_pei'),
    path('relatorio-pei/<int:neurodivergente_id>/', gerar_relatorio_pei_pdf, name='gerar_relatorio_pei_pdf'),
    path('anamnese/<int:anamnese_id>/imprimir/', imprimir_anamnese, name='imprimir_anamnese'),
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)