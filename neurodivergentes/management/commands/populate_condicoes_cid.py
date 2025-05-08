from django.core.management.base import BaseCommand
from django.db import transaction
from clientes.models import Cliente
from neurodivergentes.models import CategoriaNeurodivergente, CondicaoNeurodivergente
from django_multitenant.utils import set_current_tenant


class Command(BaseCommand):
    help = 'Popula as tabelas de categorias e condições neurodivergentes para todos os clientes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cliente_id',
            type=int,
            help='ID específico do cliente para popular as tabelas (opcional)'
        )

    def handle(self, *args, **options):
        cliente_id = options.get('cliente_id')
        
        # Define as categorias padrão
        categorias_data = [
            {'id': 1, 'nome': 'Transtornos da Comunicação e Linguagem', 'descricao': 'Esses transtornos afetam a capacidade de uma pessoa de se comunicar efetivamente, seja na fala, linguagem ou comunicação social. Exemplos incluem gagueira, mutismo seletivo, transtorno de comunicação social e transtorno do desenvolvimento da fala e linguagem.', 'ordem': 1},
            {'id': 2, 'nome': 'Transtornos de Aprendizagem', 'descricao': 'Esses transtornos se caracterizam por dificuldades específicas em determinadas habilidades de aprendizagem, como matemática (discalculia), escrita (disgrafia, disortografia) e leitura (dislexia). Também pode incluir o transtorno de aprendizagem não verbal.', 'ordem': 2},
            {'id': 3, 'nome': 'Transtornos do Neurodesenvolvimento', 'descricao': 'Esta categoria inclui condições como Altas Habilidades/Superdotação, Deficiência Intelectual, síndromes como Asperger e Down, e transtornos como TDAH e TEA, que afetam o desenvolvimento neurológico.', 'ordem': 3},
            {'id': 4, 'nome': 'Transtornos Emocionais e Comportamentais', 'descricao': 'Esses transtornos envolvem desafios nas áreas emocional e comportamental, como depressão, ansiedade, esquizofrenia, transtorno bipolar, transtorno de conduta, etc.', 'ordem': 4},
            {'id': 5, 'nome': 'Transtornos Motores', 'descricao': 'Incluem condições que afetam o desenvolvimento e o controle dos movimentos, como dispraxia e transtorno do desenvolvimento da coordenação.', 'ordem': 5},
            {'id': 6, 'nome': 'Transtornos Neurológicos', 'descricao': 'São transtornos relacionados a condições neurológicas, como epilepsia e síndrome de Tourette.', 'ordem': 6},
            {'id': 7, 'nome': 'Transtornos de Processamento', 'descricao': 'Envolvem dificuldades no processamento de informações sensoriais, auditivas, visuais e de memória.', 'ordem': 7},
            {'id': 8, 'nome': 'Transtornos Mistos/Em Investigação', 'descricao': 'Esta categoria abrange condições ainda em investigação ou que não se enquadram claramente em uma única categoria.', 'ordem': 8},
            {'id': 9, 'nome': 'Deficiência Física', 'descricao': 'Incluem condições que afetam o desenvolvimento e o controle dos movimentos, como amputação ou ausência adquirida de membros.', 'ordem': 9},
            {'id': 10, 'nome': 'Deficiência Auditiva', 'descricao': 'Deficiência auditiva a limitação de longo prazo da audição, unilateral total ou bilateral parcial ou total, a qual, em interação com uma ou mais barreiras, obstrui a participação plena e efetiva da pessoa na sociedade, em igualdade de condições com as demais pessoas.', 'ordem': 10},
            {'id': 11, 'nome': 'Doenças do sistema circulatório', 'descricao': 'Grupo de doenças cerebrovasculares', 'ordem': 11},
            {'id': 12, 'nome': 'Toxoplasmose', 'descricao': 'Toxoplasmose', 'ordem': 12},
        ]
        
        # Define as condições padrão
        condicoes_data = [
            {'id': 1, 'nome': 'Gagueira', 'cid_10': 'F98.5', 'descricao': 'Interrupção no fluxo normal da fala, caracterizada por repetições, prolongamentos e bloqueios de sons, sílabas ou palavras.', 'ativo': True, 'categoria_id': 1},
            {'id': 2, 'nome': 'Discalculia', 'cid_10': 'F81.2', 'descricao': 'Dificuldade específica no aprendizado e desempenho de habilidades matemáticas.', 'ativo': True, 'categoria_id': 2},
            {'id': 3, 'nome': 'Altas Habilidades/Superdotação', 'cid_10': 'Z91.8', 'descricao': 'Capacidade intelectual acima da média, com destaque em uma ou mais áreas.', 'ativo': True, 'categoria_id': 3},
            {'id': 4, 'nome': 'Depressão Infantil e Adolescente', 'cid_10': 'F32 ou F33', 'descricao': 'Transtorno do humor caracterizado por tristeza persistente, baixa autoestima e perda de interesse em atividades.', 'ativo': True, 'categoria_id': 4},
            {'id': 5, 'nome': 'Dispraxia', 'cid_10': 'F82', 'descricao': 'Transtorno do desenvolvimento motor que afeta a coordenação e o planejamento dos movimentos.', 'ativo': True, 'categoria_id': 5},
            {'id': 6, 'nome': 'Epilepsia', 'cid_10': 'G40', 'descricao': 'Condição neurológica crônica caracterizada por crises epilépticas recorrentes.', 'ativo': True, 'categoria_id': 6},
            {'id': 7, 'nome': 'Distúrbios de Memória', 'cid_10': 'R41.3', 'descricao': 'Dificuldades na aquisição, armazenamento ou recuperação de informações na memória.', 'ativo': True, 'categoria_id': 7},
            {'id': 8, 'nome': 'Em Investigação', 'cid_10': 'Z03.9', 'descricao': 'Quando a condição não se encaixa claramente em uma categoria diagnóstica específica.', 'ativo': True, 'categoria_id': 8},
            {'id': 9, 'nome': 'Mutismo Seletivo', 'cid_10': 'F94.0', 'descricao': 'Incapacidade persistente de falar em situações sociais específicas, apesar da capacidade de falar em outras situações.', 'ativo': True, 'categoria_id': 1},
            {'id': 10, 'nome': 'Transtorno de Comunicação Social', 'cid_10': 'F80.8', 'descricao': 'Dificuldade em usar a comunicação verbal e não verbal apropriadamente em interações sociais.', 'ativo': True, 'categoria_id': 1},
            {'id': 11, 'nome': 'Transtorno do Desenvolvimento da Fala e Linguagem', 'cid_10': 'F80.9', 'descricao': 'Dificuldades no desenvolvimento típico da fala e/ou linguagem, sem causa aparente.', 'ativo': True, 'categoria_id': 1},
            {'id': 12, 'nome': 'Transtorno Específico da Linguagem (TEL/DEL)', 'cid_10': 'F80.2', 'descricao': 'Dificuldade significativa no desenvolvimento da linguagem, sem outros déficits cognitivos.', 'ativo': True, 'categoria_id': 1},
            {'id': 13, 'nome': 'Disgrafia', 'cid_10': 'F81.1', 'descricao': 'Dificuldade no aprendizado e execução da escrita, resultando em letra ilegível e desordenada.', 'ativo': True, 'categoria_id': 2},
            {'id': 14, 'nome': 'Dislexia', 'cid_10': 'F81.0', 'descricao': 'Dificuldade específica no aprendizado e desempenho da leitura, caracterizada por erros e lentidão na leitura.', 'ativo': True, 'categoria_id': 2},
            {'id': 15, 'nome': 'Disortografia', 'cid_10': 'F81.8', 'descricao': 'Dificuldade na expressão escrita, resultando em erros ortográficos.', 'ativo': True, 'categoria_id': 2},
            {'id': 16, 'nome': 'Transtorno de Aprendizagem Não-Verbal (TANV)', 'cid_10': 'F81.9', 'descricao': 'Dificuldade no processamento e compreensão de informações não verbais.', 'ativo': True, 'categoria_id': 2},
            {'id': 17, 'nome': 'Transtornos de Habilidades Escolares', 'cid_10': 'F81', 'descricao': 'Dificuldades específicas em áreas acadêmicas como leitura, escrita e matemática.', 'ativo': True, 'categoria_id': 2},
            {'id': 18, 'nome': 'Deficiência Intelectual', 'cid_10': 'F70-F79', 'descricao': 'Funcionamento intelectual significativamente abaixo da média, com impactos no comportamento adaptativo.', 'ativo': True, 'categoria_id': 3},
            {'id': 19, 'nome': 'Síndrome de Asperger', 'cid_10': 'F84.5', 'descricao': 'Transtorno do espectro autista caracterizado por dificuldades na interação social e padrões restritos de comportamento.', 'ativo': True, 'categoria_id': 3},
            {'id': 20, 'nome': 'Síndrome de Down', 'cid_10': 'Q90', 'descricao': 'Transtorno genético causado pela presença de um cromossomo 21 extra, associado a atraso no desenvolvimento.', 'ativo': True, 'categoria_id': 3},
            {'id': 21, 'nome': 'Síndrome de Rett', 'cid_10': 'F84.2', 'descricao': 'Transtorno do neurodesenvolvimento predominante em meninas, com regressão de habilidades após um período de desenvolvimento aparentemente normal.', 'ativo': True, 'categoria_id': 3},
            {'id': 22, 'nome': 'TDAH/TDA', 'cid_10': 'F90.0', 'descricao': 'Transtorno caracterizado por desatenção, hiperatividade e impulsividade, com impacto no funcionamento diário.', 'ativo': True, 'categoria_id': 3},
            {'id': 23, 'nome': 'Transtorno do Espectro Autista (TEA)', 'cid_10': 'F84.0', 'descricao': 'Transtorno do neurodesenvolvimento caracterizado por dificuldades na comunicação, interação social e comportamentos repetitivos.', 'ativo': True, 'categoria_id': 3},
            {'id': 24, 'nome': 'Transtorno Global do Desenvolvimento Sem Outra Especificação', 'cid_10': 'F84.9', 'descricao': 'Transtorno do neurodesenvolvimento que não se enquadra em outras categorias específicas.', 'ativo': True, 'categoria_id': 3},
            {'id': 25, 'nome': 'Transtorno Hipercinético', 'cid_10': 'F90.9', 'descricao': 'Transtorno caracterizado por desatenção, hiperatividade e impulsividade.', 'ativo': True, 'categoria_id': 3},
            {'id': 26, 'nome': 'Esquizofrenia', 'cid_10': 'F20', 'descricao': 'Transtorno mental grave caracterizado por delírios, alucinações, desorganização do pensamento e do comportamento.', 'ativo': True, 'categoria_id': 4},
            {'id': 27, 'nome': 'Fobia Escolar', 'cid_10': 'F93.0', 'descricao': 'Medo intenso e irracional de ambientes escolares, levando a evitação e ausências escolares.', 'ativo': True, 'categoria_id': 4},
            {'id': 28, 'nome': 'Transtorno Bipolar', 'cid_10': 'F31', 'descricao': 'Transtorno do humor caracterizado por alternância entre episódios de mania e depressão.', 'ativo': True, 'categoria_id': 4},
            {'id': 29, 'nome': 'Transtorno de Ansiedade Generalizada (TAG)', 'cid_10': 'F41.1', 'descricao': 'Ansiedade e preocupação excessivas e persistentes sobre vários aspectos da vida.', 'ativo': True, 'categoria_id': 4},
            {'id': 30, 'nome': 'Transtorno de Conduta', 'cid_10': 'F91', 'descricao': 'Padrão persistente de comportamento desafiador, agressivo ou antissocial, com violação dos direitos dos outros.', 'ativo': True, 'categoria_id': 4},
            {'id': 31, 'nome': 'Transtorno de Desregulação do Humor com Disforia', 'cid_10': 'F34.8', 'descricao': 'Transtorno caracterizado por humor irritável, raiva e desregulação emocional.', 'ativo': True, 'categoria_id': 4},
            {'id': 32, 'nome': 'Transtorno de Estresse Pós-Traumático (TEPT)', 'cid_10': 'F43.1', 'descricao': 'Transtorno mental causado pela exposição a um evento traumático, com sintomas persistentes de revivência, evitação e hiperexcitação.', 'ativo': True, 'categoria_id': 4},
            {'id': 33, 'nome': 'Transtorno Obsessivo-Compulsivo (TOC)', 'cid_10': 'F42.9', 'descricao': 'Transtorno caracterizado por pensamentos intrusivos (obsessões) e comportamentos repetitivos (compulsões).', 'ativo': True, 'categoria_id': 4},
            {'id': 34, 'nome': 'Transtorno Opositivo-Desafiador (TOD)', 'cid_10': 'F91.3', 'descricao': 'Padrão persistente de comportamento negativo, desafiador, desobediente e hostil em relação a figuras de autoridade.', 'ativo': True, 'categoria_id': 4},
            {'id': 35, 'nome': 'Transtorno do Desenvolvimento da Coordenação (TDC)', 'cid_10': 'F82.9', 'descricao': 'Dificuldade no desenvolvimento e execução de habilidades motoras coordenadas.', 'ativo': True, 'categoria_id': 5},
            {'id': 36, 'nome': 'Síndrome de Tourette', 'cid_10': 'F95.2', 'descricao': 'Transtorno neurológico caracterizado por tiques motores e vocais involuntários.', 'ativo': True, 'categoria_id': 6},
            {'id': 37, 'nome': 'Transtorno de Processamento Auditivo (TPA)', 'cid_10': 'H93.2', 'descricao': 'Dificuldade em processar e interpretar informações auditivas.', 'ativo': True, 'categoria_id': 7},
            {'id': 38, 'nome': 'Transtorno de Processamento Sensorial (TPS)', 'cid_10': 'F88', 'descricao': 'Dificuldade em organizar e integrar adequadamente as informações sensoriais.', 'ativo': True, 'categoria_id': 7},
            {'id': 39, 'nome': 'Transtorno de Processamento Visual', 'cid_10': 'H53.9', 'descricao': 'Dificuldade em processar e interpretar informações visuais.', 'ativo': True, 'categoria_id': 7},
            {'id': 40, 'nome': 'Transtorno Misto do Desenvolvimento', 'cid_10': 'F83', 'descricao': 'Quando a pessoa apresenta uma combinação de transtornos do neurodesenvolvimento que não se enquadram em uma categoria única.', 'ativo': True, 'categoria_id': 8},
            {'id': 41, 'nome': 'Ausência adquirida de dedo(s) da mão unilateral', 'cid_10': 'Z89.0', 'descricao': 'Ausência adquirida de dedo(s) da mão unilateral.', 'ativo': True, 'categoria_id': 9},
            {'id': 42, 'nome': 'Outros transtornos comportamentais e emocionais com início habitualmente durante a infância ou a adolescência.', 'cid_10': 'F98', 'descricao': 'Outros transtornos comportamentais e emocionais com início habitualmente durante a infância ou a adolescência.', 'ativo': True, 'categoria_id': 4},
            {'id': 43, 'nome': 'Transtornos do globo ocular - Miopia degenerativa', 'cid_10': 'H442', 'descricao': 'Miopia degenerativa', 'ativo': True, 'categoria_id': 7},
            {'id': 44, 'nome': 'Síndrome de Rauch-Steindl', 'cid_10': 'Q99', 'descricao': 'Retardo no crescimento pôndero-estatural, atraso do desenvolvimento neuropsicomotor, dismorfismos faciais e deficiência intelectual.', 'ativo': True, 'categoria_id': 5},
            {'id': 45, 'nome': 'Hiperatividade', 'cid_10': 'R46.3', 'descricao': 'Transtorno que se manifesta através de um padrão persistente de desatenção, hiperatividade e impulsividade. Pessoas com hiperatividade tendem a ter dificuldade em se concentrar, controlar seus impulsos e moderar seu comportamento. Esses sintomas podem interferir significativamente na vida diária do indivíduo, afetando seu desempenho acadêmico, profissional e social.', 'ativo': True, 'categoria_id': 3},
            {'id': 47, 'nome': 'Perda de audição bilateral neurossensorial', 'cid_10': 'H90.3', 'descricao': 'Perda de audição bilateral neurossensorial', 'ativo': True, 'categoria_id': 10},
            {'id': 48, 'nome': 'Acidente Vascular Cerebral (AVC)', 'cid_10': 'I64', 'descricao': 'Acidente Vascular Cerebral (AVC) não especificado como hemorrágico ou isquêmico.', 'ativo': True, 'categoria_id': 11},
            {'id': 49, 'nome': 'Toxoplasmose', 'cid_10': 'B58.0', 'descricao': 'Toxoplasmose', 'ativo': True, 'categoria_id': 12},
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
                # Verifica se o cliente já tem categorias cadastradas
                existing_categorias = CategoriaNeurodivergente.objects.filter(cliente=cliente).count()
                
                if existing_categorias > 0:
                    self.stdout.write(f'  - Cliente {cliente.nome} já possui {existing_categorias} categorias cadastradas')
                else:
                    # Cria as categorias para este cliente
                    for categoria_data in categorias_data:
                        CategoriaNeurodivergente.objects.create(
                            cliente=cliente,
                            nome=categoria_data['nome'],
                            descricao=categoria_data['descricao'],
                            ordem=categoria_data['ordem']
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'  - {len(categorias_data)} categorias criadas para o cliente {cliente.nome}'))
                    
                    # Obtém as categorias recém-criadas para usar seus IDs
                    categorias = {c.nome: c for c in CategoriaNeurodivergente.objects.filter(cliente=cliente)}
                    
                    # Cria as condições para este cliente
                    for condicao_data in condicoes_data:
                        categoria_nome = next((c['nome'] for c in categorias_data if c['id'] == condicao_data['categoria_id']), None)
                        if categoria_nome and categoria_nome in categorias:
                            CondicaoNeurodivergente.objects.create(
                                cliente=cliente,
                                categoria=categorias[categoria_nome],
                                nome=condicao_data['nome'],
                                cid_10=condicao_data['cid_10'],
                                descricao=condicao_data['descricao'],
                                ativo=condicao_data['ativo']
                            )
                    
                    self.stdout.write(self.style.SUCCESS(f'  - {len(condicoes_data)} condições criadas para o cliente {cliente.nome}'))
        
        self.stdout.write(self.style.SUCCESS('Processo concluído com sucesso!'))
