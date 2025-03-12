from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'pia_config/login.html'
    next_page = '/dashboard/'
    
    def form_invalid(self, form):
        messages.error(self.request, 'Credenciais incorretas. Verifique seu nome de usuário e senha e tente novamente.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        
        if remember_me:
            # Define a sessão para expirar em 2 semanas
            self.request.session.set_expiry(1209600)
        else:
            # A sessão expira ao fechar o navegador
            self.request.session.set_expiry(0)
            
        return super().form_valid(form)

@login_required
def dashboard(request):
    context = {
        'show_dashboard_messages': True
    }
    return render(request, 'admin/index.html', context)