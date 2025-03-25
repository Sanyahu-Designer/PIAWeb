from django.urls import path
from . import views

app_name = 'profissionais_app'

urlpatterns = [
    path('', views.index, name='index'),
]