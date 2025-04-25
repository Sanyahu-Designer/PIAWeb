from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def politica_privacidade(request):
    """View institucional para exibir a Política de Privacidade/LGPD."""
    return render(request, 'institucional/lgpd.html')
