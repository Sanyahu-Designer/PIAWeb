from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve, reverse

class RedirectLoginMiddleware:
    """
    Middleware para interceptar redirecionamentos para a página de login
    quando o usuário já está autenticado, e substituí-los por um redirecionamento
    para o dashboard com uma mensagem de permissão negada.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Verifica se a resposta é um redirecionamento para a página de login
        if (response.status_code == 302 and 
            'login' in response.url and 
            request.user.is_authenticated):
            
            # Adiciona uma mensagem de aviso
            messages.warning(
                request, 
                'Você não tem permissão para acessar esta página. '
                'Se você acredita que isso é um erro, entre em contato com o administrador da instituição.'
            )
            
            # Redireciona para o dashboard
            return redirect('/dashboard/')
        
        return response
