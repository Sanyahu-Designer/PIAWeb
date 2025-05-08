from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm, PrimeiroUsuarioForm, EditarClienteUsuarioForm
from .models import Cliente
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group, Permission
from .models_profile import Profile
from django.db import transaction
from django.views.decorators.http import require_POST
from configuracoes.models import ConfiguracaoCliente
from django.contrib import messages

def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')(view_func))
    return decorated_view_func

@superuser_required
@transaction.atomic
def nova_prefeitura(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        user_form = PrimeiroUsuarioForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            cliente = form.save()
            # Cria o usuário admin inicial
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            password = user_form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True
            user.save()
            # Cria o profile já vinculado à prefeitura
            Profile.objects.create(user=user, cliente=cliente)

            # Cria ou obtém o grupo 'Admin da Prefeitura' e atribui permissões
            grupo, created = Group.objects.get_or_create(name='Admin da Prefeitura')
            if created or grupo.permissions.count() == 0:
                # Dá todas as permissões de add, change, delete, view para todos os models do app 'clientes'
                app_labels = ['clientes', 'neurodivergentes', 'adaptacao_curricular', 'escola', 'profissionais_app', 'bncc', 'cid10', 'metashabilidades', 'auth', 'configuracoes']
                for app_label in app_labels:
                    perms = Permission.objects.filter(content_type__app_label=app_label)
                    grupo.permissions.add(*perms)
            user.groups.add(grupo)
            
            # Popula as séries cursadas para o novo cliente
            from django_multitenant.utils import set_current_tenant
            from neurodivergentes.models.historico_escolar import SeriesCursadas
            from neurodivergentes.models import CategoriaNeurodivergente, CondicaoNeurodivergente
            
            # Define o tenant atual para este cliente
            set_current_tenant(cliente)
            
            # Define as séries e categorias padrão
            series_data = [
                {'nome': 'bercario1', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 1},
                {'nome': 'bercario2', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 2},
                {'nome': 'maternal1', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 3},
                {'nome': 'maternal2', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 4},
                {'nome': 'pre1', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 5},
                {'nome': 'pre2', 'categoria': 'EDUCAÇÃO INFANTIL', 'ordem': 6},
                {'nome': '1ano', 'categoria': 'ENSINO FUNDAMENTAL I', 'ordem': 7},
                {'nome': '2ano', 'categoria': 'ENSINO FUNDAMENTAL I', 'ordem': 8},
                {'nome': '3ano', 'categoria': 'ENSINO FUNDAMENTAL I', 'ordem': 9},
                {'nome': '4ano', 'categoria': 'ENSINO FUNDAMENTAL I', 'ordem': 10},
                {'nome': '5ano', 'categoria': 'ENSINO FUNDAMENTAL I', 'ordem': 11},
                {'nome': '6ano', 'categoria': 'ENSINO FUNDAMENTAL II', 'ordem': 12},
                {'nome': '7ano', 'categoria': 'ENSINO FUNDAMENTAL II', 'ordem': 13},
                {'nome': '8ano', 'categoria': 'ENSINO FUNDAMENTAL II', 'ordem': 14},
                {'nome': '9ano', 'categoria': 'ENSINO FUNDAMENTAL II', 'ordem': 15},
            ]
            
            # Cria as séries para este cliente
            for serie_data in series_data:
                SeriesCursadas.objects.create(
                    cliente=cliente,
                    nome=serie_data['nome'],
                    categoria=serie_data['categoria'],
                    ordem=serie_data['ordem']
                )
                
            # Define as categorias neurodivergentes padrão
            categorias_data = [
                {'nome': 'Transtornos da Comunicação e Linguagem', 'descricao': 'Esses transtornos afetam a capacidade de uma pessoa de se comunicar efetivamente, seja na fala, linguagem ou comunicação social.', 'ordem': 1},
                {'nome': 'Transtornos de Aprendizagem', 'descricao': 'Esses transtornos se caracterizam por dificuldades específicas em determinadas habilidades de aprendizagem.', 'ordem': 2},
                {'nome': 'Transtornos do Neurodesenvolvimento', 'descricao': 'Esta categoria inclui condições como Altas Habilidades/Superdotação, Deficiência Intelectual, síndromes como Asperger e Down, e transtornos como TDAH e TEA.', 'ordem': 3},
                {'nome': 'Transtornos Emocionais e Comportamentais', 'descricao': 'Esses transtornos envolvem desafios nas áreas emocional e comportamental.', 'ordem': 4},
                {'nome': 'Transtornos Motores', 'descricao': 'Incluem condições que afetam o desenvolvimento e o controle dos movimentos.', 'ordem': 5},
                {'nome': 'Transtornos Neurológicos', 'descricao': 'São transtornos relacionados a condições neurológicas.', 'ordem': 6},
                {'nome': 'Transtornos de Processamento', 'descricao': 'Envolvem dificuldades no processamento de informações sensoriais, auditivas, visuais e de memória.', 'ordem': 7},
                {'nome': 'Transtornos Mistos/Em Investigação', 'descricao': 'Esta categoria abrange condições ainda em investigação ou que não se enquadram claramente em uma única categoria.', 'ordem': 8},
                {'nome': 'Deficiência Física', 'descricao': 'Incluem condições que afetam o desenvolvimento e o controle dos movimentos, como amputação ou ausência adquirida de membros.', 'ordem': 9},
                {'nome': 'Deficiência Auditiva', 'descricao': 'Deficiência auditiva a limitação de longo prazo da audição, unilateral total ou bilateral parcial ou total.', 'ordem': 10},
                {'nome': 'Doenças do sistema circulatório', 'descricao': 'Grupo de doenças cerebrovasculares', 'ordem': 11},
                {'nome': 'Toxoplasmose', 'descricao': 'Toxoplasmose', 'ordem': 12},
            ]
            
            # Cria as categorias para este cliente
            categorias = {}
            for categoria_data in categorias_data:
                categoria = CategoriaNeurodivergente.objects.create(
                    cliente=cliente,
                    nome=categoria_data['nome'],
                    descricao=categoria_data['descricao'],
                    ordem=categoria_data['ordem']
                )
                categorias[categoria_data['nome']] = categoria
            
            # Define as condições neurodivergentes padrão (apenas algumas das mais comuns para não sobrecarregar a função)
            condicoes_data = [
                {'nome': 'Gagueira', 'cid_10': 'F98.5', 'descricao': 'Interrupção no fluxo normal da fala.', 'categoria': 'Transtornos da Comunicação e Linguagem'},
                {'nome': 'Discalculia', 'cid_10': 'F81.2', 'descricao': 'Dificuldade específica no aprendizado e desempenho de habilidades matemáticas.', 'categoria': 'Transtornos de Aprendizagem'},
                {'nome': 'Dislexia', 'cid_10': 'F81.0', 'descricao': 'Dificuldade específica no aprendizado e desempenho da leitura.', 'categoria': 'Transtornos de Aprendizagem'},
                {'nome': 'TDAH/TDA', 'cid_10': 'F90.0', 'descricao': 'Transtorno caracterizado por desatenção, hiperatividade e impulsividade.', 'categoria': 'Transtornos do Neurodesenvolvimento'},
                {'nome': 'Transtorno do Espectro Autista (TEA)', 'cid_10': 'F84.0', 'descricao': 'Transtorno do neurodesenvolvimento caracterizado por dificuldades na comunicação, interação social e comportamentos repetitivos.', 'categoria': 'Transtornos do Neurodesenvolvimento'},
                {'nome': 'Síndrome de Down', 'cid_10': 'Q90', 'descricao': 'Transtorno genético causado pela presença de um cromossomo 21 extra.', 'categoria': 'Transtornos do Neurodesenvolvimento'},
                {'nome': 'Depressão Infantil e Adolescente', 'cid_10': 'F32 ou F33', 'descricao': 'Transtorno do humor caracterizado por tristeza persistente.', 'categoria': 'Transtornos Emocionais e Comportamentais'},
                {'nome': 'Transtorno de Ansiedade Generalizada (TAG)', 'cid_10': 'F41.1', 'descricao': 'Ansiedade e preocupação excessivas e persistentes.', 'categoria': 'Transtornos Emocionais e Comportamentais'},
                {'nome': 'Epilepsia', 'cid_10': 'G40', 'descricao': 'Condição neurológica crônica caracterizada por crises epilépticas recorrentes.', 'categoria': 'Transtornos Neurológicos'},
                {'nome': 'Acidente Vascular Cerebral (AVC)', 'cid_10': 'I64', 'descricao': 'AVC não especificado como hemorrágico ou isquêmico.', 'categoria': 'Doenças do sistema circulatório'},
            ]
            
            # Cria as condições para este cliente
            for condicao_data in condicoes_data:
                if condicao_data['categoria'] in categorias:
                    CondicaoNeurodivergente.objects.create(
                        cliente=cliente,
                        categoria=categorias[condicao_data['categoria']],
                        nome=condicao_data['nome'],
                        cid_10=condicao_data['cid_10'],
                        descricao=condicao_data['descricao'],
                        ativo=True
                    )

            return redirect('listar_clientes')
    else:
        form = ClienteForm()
        user_form = PrimeiroUsuarioForm()
    return render(request, 'clientes/nova_prefeitura.html', {'form': form, 'user_form': user_form})

@superuser_required
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})

@superuser_required
def ver_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/ver_cliente.html', {'cliente': cliente})

@login_required
def listar_usuarios_cliente(request, cliente_id):
    # Verifica se o usuário é superusuário ou está no modo de impersonação
    if not request.user.is_superuser and not hasattr(request, 'is_impersonating'):
        return redirect('login')
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Lista apenas usuários com Profile vinculado à prefeitura E que NÃO sejam superusuários
    perfis = cliente.profile_set.select_related('user')
    usuarios = [profile.user for profile in perfis if not profile.user.is_superuser]
    return render(request, 'clientes/listar_usuarios.html', {'usuarios': usuarios, 'cliente': cliente})

@superuser_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Busca o usuário admin vinculado a este cliente (Profile)
    try:
        profile = cliente.profile_set.first()
        user = profile.user if profile else None
    except Exception:
        user = None
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        user_form = EditarClienteUsuarioForm(request.POST, initial={'username': user.username if user else '', 'email': user.email if user else '', 'first_name': user.first_name if user else '', 'last_name': user.last_name if user else ''})
        if form.is_valid() and user_form.is_valid():
            form.save()
            if user:
                user.username = user_form.cleaned_data['username']
                user.email = user_form.cleaned_data['email']
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                if user_form.cleaned_data['password']:
                    user.set_password(user_form.cleaned_data['password'])
                user.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
        if user:
            user_form = EditarClienteUsuarioForm(initial={'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name})
        else:
            user_form = EditarClienteUsuarioForm()
    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente, 'user_form': user_form})

@superuser_required
def confirmar_excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/confirmar_excluir_cliente.html', {'cliente': cliente})

@superuser_required
@require_POST
def excluir_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    # Exclui todos os perfis e usuários vinculados a este cliente
    perfis = cliente.profile_set.all()
    for profile in perfis:
        user = profile.user
        profile.delete()
        user.delete()
    cliente.delete()
    return redirect('listar_clientes')

@login_required
def impersonate_cliente(request, cliente_id):
    # Apenas superusuários podem impersonar
    if not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para realizar esta ação.")
        return redirect('listar_clientes')
    
    # Busca o cliente pelo ID
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Registrar a mudança de tenant no log de auditoria
    from clientes.audit import log_tenant_switch
    old_cliente = None
    if 'impersonated_cliente_id' in request.session:
        try:
            old_cliente = Cliente.objects.get(id=request.session['impersonated_cliente_id'])
        except Cliente.DoesNotExist:
            pass
    log_tenant_switch(request, old_cliente, cliente)
    
    # Guarda as informações do cliente na sessão
    request.session['impersonated_cliente_id'] = cliente.id
    request.session['impersonated_cliente_name'] = cliente.nome
    
    messages.success(request, f"Você está visualizando o sistema como {cliente.nome}")
    return redirect('dashboard')

@login_required
def stop_impersonation(request):
    # Registrar a mudança de tenant no log de auditoria
    from clientes.audit import log_tenant_switch
    old_cliente = None
    if 'impersonated_cliente_id' in request.session:
        try:
            old_cliente = Cliente.objects.get(id=request.session['impersonated_cliente_id'])
        except Cliente.DoesNotExist:
            pass
    log_tenant_switch(request, old_cliente, None)
    
    # Remove as informações de impersonação da sessão
    if 'impersonated_cliente_id' in request.session:
        del request.session['impersonated_cliente_id']
    if 'impersonated_cliente_name' in request.session:
        del request.session['impersonated_cliente_name']
    
    messages.success(request, "Você saiu do modo de visualização de prefeitura.")
    return redirect('listar_clientes')
