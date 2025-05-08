from django.core.management.base import BaseCommand
from django.db import transaction
from clientes.models import Cliente
from neurodivergentes.models.historico_escolar import SeriesCursadas
from django_multitenant.utils import set_current_tenant


class Command(BaseCommand):
    help = 'Popula a tabela SeriesCursadas para todos os clientes existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cliente_id',
            type=int,
            help='ID específico do cliente para popular as séries cursadas (opcional)'
        )

    def handle(self, *args, **options):
        cliente_id = options.get('cliente_id')
        
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
        
        # Filtra clientes se um ID específico foi fornecido
        if cliente_id:
            clientes = Cliente.objects.filter(id=cliente_id)
            if not clientes.exists():
                self.stdout.write(self.style.ERROR(f'Cliente com ID {cliente_id} não encontrado'))
                return
        else:
            clientes = Cliente.objects.all()
        
        for cliente in clientes:
            self.stdout.write(f'Processando cliente: {cliente.nome}')
            
            # Define o tenant atual para este cliente
            set_current_tenant(cliente)
            
            with transaction.atomic():
                # Verifica se já existem séries para este cliente
                existing_series = SeriesCursadas.objects.filter(cliente=cliente)
                if existing_series.exists():
                    self.stdout.write(f'  - Cliente {cliente.nome} já possui {existing_series.count()} séries cadastradas')
                    continue
                
                # Cria as séries para este cliente
                for serie_data in series_data:
                    SeriesCursadas.objects.create(
                        cliente=cliente,
                        nome=serie_data['nome'],
                        categoria=serie_data['categoria'],
                        ordem=serie_data['ordem']
                    )
                
                self.stdout.write(self.style.SUCCESS(f'  - {len(series_data)} séries criadas para o cliente {cliente.nome}'))
        
        self.stdout.write(self.style.SUCCESS('Processo concluído com sucesso!'))
