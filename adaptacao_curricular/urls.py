from django.urls import path
from . import views

app_name = 'adaptacao_curricular'

urlpatterns = [
    path('adaptacao/<int:adaptacao_id>/disciplina/<int:disciplina_id>/imprimir/',
         views.imprimir_adaptacao_disciplina,
         name='imprimir_adaptacao_disciplina'),
    path('adaptacao/habilidade/<int:adaptacao_habilidade_id>/imprimir/',
         views.imprimir_adaptacao_habilidade,
         name='imprimir_adaptacao_habilidade'),
]
