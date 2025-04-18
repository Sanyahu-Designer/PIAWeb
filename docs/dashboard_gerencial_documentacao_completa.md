# Documentação Completa do Dashboard Gerencial

## Visão Geral
O Dashboard Gerencial do sistema PIA (Plano Individual de Aprendizagem) foi desenvolvido para fornecer uma visão abrangente e detalhada sobre os alunos neurodivergentes, profissionais e escolas. Utilizando visualizações interativas e dados em tempo real, o dashboard permite que gestores tomem decisões baseadas em dados concretos, identificando tendências, monitorando o progresso dos alunos e otimizando a alocação de recursos.

## Aspectos Técnicos e Visuais
- **Paleta de Cores:** Utiliza cores pastel para todos os gráficos, proporcionando uma experiência visual agradável e consistente.
- **Fonte:** Todos os textos utilizam a fonte Roboto, conforme o padrão do Material Dashboard 3.
- **Responsividade:** O dashboard é totalmente responsivo, adaptando-se a diferentes tamanhos de tela.
- **Interatividade:** Todos os gráficos possuem tooltips que mostram informações detalhadas ao passar o mouse sobre os elementos.
- **Acessibilidade:** As cores foram escolhidas para garantir contraste adequado, e todos os elementos possuem textos alternativos.

## Gráficos e Visualizações

### 1. Gráfico de Distribuição por Gênero
**Descrição:** Apresenta a distribuição dos alunos/pacientes por gênero (Masculino/Feminino).

**Tipo de Gráfico:** Gráfico de pizza.

**Fonte de Dados:** API `/api/genero-por-neurodivergencia/` que retorna dados agregados de gênero.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Cores pastel para cada segmento
- Tooltips que mostram a porcentagem e o número absoluto

**Utilidade:** Permite visualizar rapidamente a proporção de alunos por gênero, auxiliando em análises demográficas e planejamento de recursos específicos.

### 2. Gráfico de Gênero por Neurodivergência
**Descrição:** Mostra a distribuição de gênero para cada tipo de neurodivergência.

**Tipo de Gráfico:** Gráfico de barras empilhadas.

**Fonte de Dados:** API `/api/genero-por-neurodivergencia/` que retorna dados cruzados de gênero e neurodivergência.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Barras empilhadas para cada neurodivergência
- Cores distintas para cada gênero
- Eixo Y com escala adaptativa

**Utilidade:** Permite identificar padrões de prevalência de neurodivergências por gênero, auxiliando em pesquisas e abordagens específicas.

### 3. Gráfico de Distribuição por Neurodivergência
**Descrição:** Apresenta a quantidade de alunos para cada tipo de neurodivergência.

**Tipo de Gráfico:** Gráfico de barras.

**Fonte de Dados:** API `/api/distribuicao-por-neurodivergencia/` que retorna a contagem de alunos por tipo de neurodivergência.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Barras com bordas arredondadas
- Cores pastel distintas para cada neurodivergência
- Tooltips que mostram o número exato de alunos

**Utilidade:** Permite visualizar quais neurodivergências são mais comuns entre os alunos atendidos, auxiliando no planejamento de capacitações e recursos.

### 4. Gráfico de Atendimentos Mensais
**Descrição:** Mostra a quantidade de atendimentos por mês, classificados por status (Ausências, Presenças, Em andamento, Iniciado, Suspenso e Cancelado).

**Tipo de Gráfico:** Gráfico de barras agrupadas.

**Fonte de Dados:** API `/api/ausencias-por-aluno/` que retorna dados mensais de atendimentos.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Barras agrupadas para cada mês
- Cores distintas para cada status de atendimento
- Filtragem para mostrar apenas meses com dados relevantes
- Escala adaptativa no eixo Y

**Utilidade:** Permite monitorar a frequência e o status dos atendimentos ao longo do ano, identificando tendências e padrões de ausência/presença.

### 5. Gráfico de Alunos por Profissional
**Descrição:** Apresenta a quantidade de alunos atendidos por cada profissional.

**Tipo de Gráfico:** Gráfico de barras horizontais.

**Fonte de Dados:** API `/api/alunos-por-profissional/` que retorna a contagem de alunos por profissional.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Barras horizontais para melhor visualização de nomes longos
- Ordenação decrescente por número de alunos
- Limite de 10 profissionais para evitar sobrecarga visual
- Tooltips que mostram o número exato de alunos

**Utilidade:** Permite visualizar a distribuição de carga de trabalho entre os profissionais, auxiliando na gestão de recursos humanos.

### 6. Gráfico de Especialização dos Profissionais
**Descrição:** Mostra a distribuição de tipos de neurodivergência atendidos por cada profissional.

**Tipo de Gráfico:** Gráfico de radar.

**Fonte de Dados:** API `/api/especializacao-profissionais/` que retorna dados sobre as especializações de cada profissional.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Gráfico de radar com múltiplos datasets (um para cada profissional)
- Cores pastel distintas para cada profissional
- Áreas semi-transparentes para melhor visualização
- Limite de 10 profissionais para evitar sobrecarga visual

**Utilidade:** Permite identificar as áreas de especialização de cada profissional, auxiliando na alocação de novos alunos e no planejamento de capacitações.

### 7. Tabela de Alerta de Alunos em Risco
**Descrição:** Apresenta informações detalhadas sobre alunos que estão em situação de risco.

**Tipo de Visualização:** Tabela interativa.

**Fonte de Dados:** API `/api/alunos-em-risco/` que retorna dados sobre alunos em diferentes categorias de risco.

**Implementação Técnica:**
- Tabela responsiva com Material Design
- Indicadores visuais de severidade (alta, média, baixa)
- Ordenação por nível de severidade
- Detalhes específicos sobre cada situação de risco

**Categorias de Risco:**
- **Ausências Consecutivas:** Alunos com 3 ou mais faltas nos últimos 90 dias
- **Sem Progresso no PDI:** Nenhum objetivo concluído nos últimos 90 dias
- **Sem Atendimento Recente:** Mais de 30 dias sem atendimento
- **Objetivos Não Alcançados:** PDIs concluídos com objetivos incompletos
- **PDI Desatualizado:** PDI sem atualização há mais de 60 dias

**Utilidade:** Permite identificar rapidamente alunos que precisam de atenção especial, facilitando intervenções proativas.

### 8. Escolas com Maior Demanda
**Descrição:** Apresenta as escolas com maior número de alunos neurodivergentes.

**Tipo de Gráfico:** Gráfico de barras horizontais.

**Fonte de Dados:** API `/api/escolas-maior-demanda/` que retorna a contagem de alunos por escola.

**Implementação Técnica:**
- Utiliza a biblioteca Chart.js para renderização
- Barras horizontais para melhor visualização de nomes longos
- Ordenação decrescente por número de alunos
- Limite das 10 escolas com maior demanda
- Tooltips que mostram o número exato de alunos

**Utilidade:** Permite identificar escolas com maior demanda, auxiliando no planejamento de recursos e parcerias.

## Arquitetura e Fluxo de Dados

### Backend (APIs)
O backend do dashboard é composto por várias APIs RESTful que fornecem dados estruturados para cada gráfico:

1. `/api/genero-por-neurodivergencia/`: Fornece dados de distribuição de gênero e neurodivergência.
2. `/api/distribuicao-por-neurodivergencia/`: Fornece dados de contagem por tipo de neurodivergência.
3. `/api/ausencias-por-aluno/`: Fornece dados mensais de atendimentos por status.
4. `/api/alunos-por-profissional/`: Fornece dados de contagem de alunos por profissional.
5. `/api/especializacao-profissionais/`: Fornece dados sobre as especializações de cada profissional.
6. `/api/alunos-em-risco/`: Fornece dados detalhados sobre alunos em situação de risco.
7. `/api/escolas-maior-demanda/`: Fornece dados de contagem de alunos por escola.

Cada API implementa:
- Autenticação via decorador `@login_required`
- Tratamento de erros com fallbacks para dados vazios
- Formatação de dados compatível com Chart.js
- Otimização de consultas ao banco de dados

### Frontend (Visualização)
O frontend utiliza:
- HTML5 e CSS3 para estrutura e estilo
- Material Dashboard 3 como framework de UI
- Chart.js para renderização de gráficos
- JavaScript para interatividade e consumo de APIs
- Fonte Roboto para tipografia
- Paleta de cores pastel para visualização agradável

## Manutenção e Extensão

### Adição de Novos Gráficos
Para adicionar um novo gráfico ao dashboard:

1. Crie uma nova API no arquivo `views.py`
2. Adicione a rota da API no arquivo `urls.py`
3. Adicione o HTML para o novo gráfico no template `dashboard_gerente.html`
4. Adicione o JavaScript para consumir a API e renderizar o gráfico

### Modificação de Gráficos Existentes
Para modificar um gráfico existente:

1. Atualize a API correspondente no arquivo `views.py`
2. Se necessário, atualize o HTML no template `dashboard_gerente.html`
3. Atualize o JavaScript que consome a API e renderiza o gráfico

## Conclusão
O Dashboard Gerencial do sistema PIA oferece uma visão abrangente e detalhada sobre alunos, profissionais e escolas, permitindo que gestores tomem decisões baseadas em dados concretos. Com visualizações interativas e dados em tempo real, o dashboard é uma ferramenta essencial para o monitoramento e a gestão eficiente do programa.
