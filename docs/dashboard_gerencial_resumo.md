# Dashboard Gerencial: Resumo dos Gráficos

## 1. Distribuição por Gênero
**Descrição:** Apresenta a distribuição dos alunos/pacientes por gênero (Masculino/Feminino).
**Tipo de Gráfico:** Gráfico de pizza.
**Quando Aparecem Dados:** Sempre que houver pelo menos um aluno cadastrado no sistema.

## 2. Gênero por Neurodivergência
**Descrição:** Mostra a distribuição de gênero para cada tipo de neurodivergência.
**Tipo de Gráfico:** Gráfico de barras empilhadas.
**Quando Aparecem Dados:** Quando existirem alunos com diagnósticos de neurodivergência cadastrados no sistema.

## 3. Distribuição por Neurodivergência
**Descrição:** Apresenta a quantidade de alunos para cada tipo de neurodivergência.
**Tipo de Gráfico:** Gráfico de barras.
**Quando Aparecem Dados:** Quando existirem diagnósticos de neurodivergência cadastrados no sistema. Se não houver diagnósticos, exibe categorias padrão (TEA, TDAH, Dislexia, Discalculia, TOD).

## 4. Atendimentos Mensais
**Descrição:** Mostra a quantidade de atendimentos por mês, classificados por status (Ausências, Presenças, Em andamento, Iniciado, Suspenso e Cancelado).
**Tipo de Gráfico:** Gráfico de barras agrupadas.
**Quando Aparecem Dados:** Quando existirem PDIs cadastrados no ano atual. O gráfico mostra apenas os meses que possuem pelo menos um atendimento em qualquer status.

## 5. Alunos por Profissional
**Descrição:** Apresenta a quantidade de alunos atendidos por cada profissional.
**Tipo de Gráfico:** Gráfico de barras horizontais.
**Quando Aparecem Dados:** Quando existirem profissionais com pelo menos um aluno associado através de PDIs. Exibe no máximo 10 profissionais ordenados pelo número de alunos.

## 6. Especialização dos Profissionais
**Descrição:** Mostra a distribuição de tipos de neurodivergência atendidos por cada profissional.
**Tipo de Gráfico:** Gráfico de radar.
**Quando Aparecem Dados:** Quando existirem profissionais com alunos que possuem diagnósticos de neurodivergência. Exibe até 10 profissionais com mais alunos, mesmo que alguns não tenham alunos com diagnósticos específicos.

## 7. Alerta de Alunos em Risco
**Descrição:** Apresenta informações detalhadas sobre alunos que estão em situação de risco.
**Tipo de Visualização:** Tabela interativa.
**Quando Aparecem Dados:** Quando existirem alunos que se enquadram em pelo menos uma das seguintes categorias de risco:
- Ausências Consecutivas (3+ faltas nos últimos 90 dias)
- Sem Progresso no PDI (nenhum objetivo concluído nos últimos 90 dias)
- Sem Atendimento Recente (mais de 30 dias sem atendimento)
- Objetivos Não Alcançados (PDIs concluídos com objetivos incompletos)
- PDI Desatualizado (sem atualização há mais de 60 dias)

## 8. Escolas com Maior Demanda
**Descrição:** Apresenta as escolas com maior número de alunos neurodivergentes.
**Tipo de Gráfico:** Gráfico de barras horizontais.
**Quando Aparecem Dados:** Quando existirem escolas com alunos neurodivergentes cadastrados. Exibe as 10 escolas com maior número de alunos.

## 9. Próximos Atendimentos
**Descrição:** Lista os PDIs ativos que estão em andamento ou iniciados.
**Tipo de Visualização:** Lista com contador.
**Quando Aparecem Dados:** Quando existirem PDIs com status "iniciado" ou "em_andamento". Exibe até 5 PDIs na lista e mostra o total de PDIs ativos.

## 10. Alunos sem Atendimento Recente
**Descrição:** Lista os alunos que estão há mais tempo sem receber atendimento.
**Tipo de Visualização:** Lista com contador.
**Quando Aparecem Dados:** Quando existirem alunos com PDIs concluídos há mais de 15 dias. Exibe até 5 alunos ordenados pelo tempo sem atendimento (do maior para o menor) e mostra o total de alunos nessa situação.
