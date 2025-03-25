from django.urls import path
from . import views

app_name = 'escola'

urlpatterns = [
    path('', views.index, name='index'),
]