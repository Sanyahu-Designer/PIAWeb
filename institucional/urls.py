from django.urls import path, re_path
from .views import politica_privacidade

urlpatterns = [
    re_path(r'^lgpd/?$', politica_privacidade, name='politica_privacidade'),
]