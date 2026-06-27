# 📋 Tasks do Projeto — Etapa 1

Cada tarefa abaixo corresponde a uma seção do `notebook_base.ipynb`.
Desenvolva no seu fork e abra um Pull Request quando concluir.

---

## ✅ Status

| # | Tarefa | Responsável | Status |
|---|--------|-------------|--------|
| 01 | Carregamento dos dados | PBergo + GitAI | ✅ Concluído |
| 02 | Inspeção inicial | PBergo + GitAI | ✅ Concluído |
| 03 | Limpeza dos dados | PBergo + GitAI | ✅ Concluído |
| 04 | Transformações | PBergo + GitAI | ✅ Concluído |
| 05 | Análise estatística descritiva | PBergo + GitAI | ✅ Concluído |
| 06 | Retorno diário | PBergo + GitAI | ✅ Concluído |
| 07 | Retorno acumulado | PBergo + GitAI | ✅ Concluído |
| 08 | Volatilidade anualizada | PBergo + GitAI | ✅ Concluído |
| 09 | Drawdown | PBergo + GitAI | ✅ Concluído |
| 10 | Índice de Sharpe | PBergo + GitAI | ✅ Concluído |
| 11 | Correlação entre ações | PBergo + GitAI | ✅ Concluído |
| 12 | Gráfico de preços e médias móveis | PBergo + GitAI | ✅ Concluído |
| 13 | Gráfico de retorno acumulado | PBergo + GitAI | ✅ Concluído |
| 14 | Histograma de retornos diários | PBergo + GitAI | ✅ Concluído |
| 15 | Boxplot comparativo de retornos | PBergo + GitAI | ✅ Concluído |
| 16 | Scatter retorno médio × volatilidade | PBergo + GitAI | ✅ Concluído |
| 17 | Mapa de calor de correlação | PBergo + GitAI | ✅ Concluído |
| 18 | Scatterplot de correlação entre pares | PBergo + GitAI | ✅ Concluído |
| 19 | Análise de volume | PBergo + GitAI | ✅ Concluído |

> Coloque seu nome na coluna **Responsável** ao pegar uma tarefa.
> Atualize o **Status** com: 🔲 Pendente · 🔄 Em andamento · ✅ Concluído

---

# 🔧 BLOCO 1 — Coleta e Tratamento

---

## 📥 01 — Carregamento dos dados

**Objetivo:** Ler os arquivos CSV/XLSX do Yahoo Finance e carregar em um DataFrame pandas.

**Instruções:**
- Os arquivos estão em `data/raw/`
- Cada arquivo corresponde a uma ação (ex: `PETR4.csv`, `VALE3.csv`)
- Carregar todos os arquivos e consolidar em um único DataFrame
- A coluna de identificação da ação deve se chamar `ticker`

**Entrega esperada:** DataFrame `dados` com todos os arquivos consolidados e coluna `ticker`.

---

## 🔍 02 — Inspeção inicial

**Objetivo:** Entender a estrutura dos dados antes de qualquer tratamento.

**Instruções:**
- Verificar shape (linhas e colunas)
- Listar tipos de dados de cada coluna
- Identificar valores ausentes
- Ver as primeiras e últimas linhas
- Executar o `.describe()` para uma visão geral das estatísticas básicas

**Entrega esperada:** Célula Markdown no notebook com um resumo do que foi encontrado — quantas linhas, quais colunas têm NaN, quais tipos estão incorretos.

---

## 🧹 03 — Limpeza dos dados

**Objetivo:** Remover ou corrigir problemas encontrados na inspeção.

**Instruções:**
- Remover linhas com valores ausentes nas colunas de preço
- Remover duplicatas
- Padronizar nomes de colunas (minúsculas, sem espaço, sem acento)
- Remover caracteres especiais de colunas numéricas (cifrão, vírgula como separador decimal)

**Entrega esperada:** DataFrame limpo, sem NaN nas colunas de preço, sem duplicatas, colunas padronizadas.

---

## 🔄 04 — Transformações

**Objetivo:** Preparar os dados para análise — tipos corretos e novas colunas úteis.

**Instruções:**
- Converter coluna de data para tipo `datetime`
- Ordenar por ticker e data
- Extrair ano e mês em colunas separadas
- Definir a data como índice

**Entrega esperada:** DataFrame com data como índice datetime, ordenado, com colunas `ano` e `mes`.

---

# 📊 BLOCO 2 — Análise Estatística

---

## 📊 05 — Análise estatística descritiva

**Objetivo:** Calcular as principais medidas estatísticas por ação.

**Instruções:**
- Calcular média, mediana, desvio padrão, mínimo e máximo do preço de fechamento
- Agrupar por ticker
- Apresentar em uma tabela formatada

**Entrega esperada:** DataFrame `resumo` com as métricas por ticker.

---

## 📈 06 — Retorno diário

**Objetivo:** Calcular o retorno percentual de um dia para o outro de cada ação.

**O que é retorno diário?**
É a variação percentual do preço de fechamento entre dois dias consecutivos.
Se o preço passou de R$ 100 para R$ 102, o retorno foi de +2%.
Preço absoluto não é comparável entre ações — retorno percentual é.

**Instruções:**
- Calcular separadamente por ticker para não misturar ações
- Remover o primeiro dia de cada ticker (gera NaN por não ter dia anterior)
- Resultado deve ficar em uma nova coluna chamada `retorno_diario`

**Entrega esperada:** Coluna `retorno_diario` no DataFrame.

---

## 📈 07 — Retorno acumulado

**Objetivo:** Mostrar quanto R$ 1,00 investido no início do período valeria ao longo do tempo em cada ação.

**O que é retorno acumulado?**
É o efeito composto dos retornos diários — multiplica os fatores de retorno dia a dia.
Permite comparar visualmente o desempenho de ações com preços absolutos muito diferentes.

**Instruções:**
- Calcular a partir do retorno diário usando produto acumulado
- Calcular separadamente por ticker
- Resultado deve ficar em uma nova coluna chamada `retorno_acumulado`

**Entrega esperada:** Coluna `retorno_acumulado` no DataFrame, partindo de 1.0 no primeiro dia de cada ticker.

---

## 📉 08 — Volatilidade anualizada

**Objetivo:** Medir o risco de cada ação de forma comparável e padronizada.

**O que é volatilidade anualizada?**
É o desvio padrão dos retornos diários multiplicado pela raiz quadrada de 252 (número de pregões no ano).
Essa conversão permite comparar a volatilidade entre ativos independentemente do período analisado.
Uma ação com volatilidade anualizada de 40% é significativamente mais arriscada que uma com 15%.

**Instruções:**
- Calcular o desvio padrão dos retornos diários por ticker
- Multiplicar por √252 para anualizar
- Apresentar em uma tabela ordenada da maior para a menor volatilidade

**Entrega esperada:** DataFrame com a volatilidade anualizada de cada ação, em ordem decrescente.

---

## 📉 09 — Drawdown

**Objetivo:** Identificar as maiores quedas de cada ação em relação ao seu pico histórico no período analisado.

**O que é drawdown?**
É a queda percentual do preço em relação ao maior valor já atingido até aquele momento.
Se uma ação chegou a R$ 100 e caiu para R$ 70, o drawdown é de -30%.
É uma medida de risco muito usada na prática porque mostra o quanto o investidor perdeu antes de a ação se recuperar.

**Instruções:**
- Calcular o pico acumulado (máximo histórico até cada data) por ticker
- Calcular o drawdown como a variação entre o preço atual e o pico
- Identificar o drawdown máximo (pior momento) de cada ação

**Entrega esperada:** Coluna `drawdown` no DataFrame e tabela com o drawdown máximo por ticker.

---

## ⚖️ 10 — Índice de Sharpe

**Objetivo:** Medir a relação entre retorno e risco de cada ação.

**O que é o Índice de Sharpe?**
É o retorno médio de um ativo dividido pela sua volatilidade.
Responde à pergunta: quanto de retorno estou recebendo por cada unidade de risco que estou assumindo?
Um Sharpe de 1.0 é considerado bom. Acima de 2.0, excelente. Negativo significa que o ativo rendeu menos que a taxa livre de risco.
Neste projeto usaremos taxa livre de risco = 0 para simplificar (Sharpe não anualizado).

**Instruções:**
- Calcular o retorno médio diário por ticker
- Dividir pelo desvio padrão dos retornos diários
- Multiplicar por √252 para anualizar
- Apresentar em tabela ordenada do maior para o menor Sharpe

**Entrega esperada:** DataFrame com o Índice de Sharpe anualizado de cada ação, em ordem decrescente.

---

## 🔗 11 — Correlação entre ações

**Objetivo:** Verificar se as ações se movem juntas ou de forma independente.

**O que é correlação?**
É um valor entre -1 e 1 que mede o quanto os retornos de duas ações se movem juntos.
1 = sempre na mesma direção · 0 = independentes · -1 = sempre em direções opostas.
Ações muito correlacionadas não diversificam o risco de uma carteira.

**Instruções:**
- Criar uma tabela pivô com os retornos diários de cada ação nas colunas
- Calcular a matriz de correlação entre todas as combinações de pares

**Entrega esperada:** DataFrame `correlacao` com a matriz de correlação entre as ações.

---

# 📈 BLOCO 3 — Visualização

---

## 📉 12 — Gráfico de preços e médias móveis

**Objetivo:** Visualizar a evolução do preço de fechamento e identificar tendências.

**O que é média móvel?**
É a média dos últimos N dias de preço. Suaviza o ruído do dia a dia e revela a tendência de fundo.
A média de 21 dias captura tendências de curto prazo. A de 200 dias, tendências de longo prazo.
Quando o preço cruza a média de 200 dias de baixo para cima, é um sinal clássico de tendência de alta.

**Instruções:**
- Um gráfico de linha por ação com o preço de fechamento
- Adicionar as médias móveis de 21 e 200 dias no mesmo gráfico
- Título, rótulos de eixo e legenda obrigatórios

**Entrega esperada:** Gráfico de linhas com preço e médias móveis para cada ação.

---

## 📈 13 — Gráfico de retorno acumulado

**Objetivo:** Comparar o desempenho de todas as ações no mesmo gráfico a partir de uma base comum.

**Instruções:**
- Todas as ações no mesmo gráfico
- Eixo Y começa em 1.0 (base comum de comparação)
- Linha horizontal tracejada em 1.0 como referência (abaixo = perda, acima = ganho)
- Título, rótulos de eixo e legenda obrigatórios

**Entrega esperada:** Gráfico de linhas com o retorno acumulado de todas as ações sobrepostas.

---

## 📊 14 — Histograma de retornos diários

**Objetivo:** Visualizar a distribuição dos retornos de cada ação.

**Instruções:**
- Um histograma por ação com curva de densidade (KDE)
- Linha vertical tracejada no zero para referência
- Permite identificar assimetria e caudas pesadas na distribuição

**Entrega esperada:** Histogramas com curva KDE e linha de referência no zero para cada ação.

---

## 📦 15 — Boxplot comparativo de retornos

**Objetivo:** Comparar a dispersão dos retornos entre as ações lado a lado.

**Instruções:**
- Um boxplot por ação no mesmo gráfico
- Permite identificar visualmente qual ação tem maior volatilidade e quais têm outliers extremos

**Entrega esperada:** Boxplot comparativo com todas as ações no mesmo gráfico.

---

## 🎯 16 — Scatter retorno médio × volatilidade

**Objetivo:** Posicionar cada ação em um mapa de risco e retorno.

**O que este gráfico mostra?**
Cada ação vira um ponto. Eixo X é a volatilidade anualizada (risco). Eixo Y é o retorno médio anualizado.
O ideal é estar no canto superior esquerdo: alto retorno com baixo risco.
Este é o gráfico mais usado em análise de carteiras para comparar ativos.

**Instruções:**
- Um ponto por ação
- Eixo X: volatilidade anualizada · Eixo Y: retorno médio anualizado
- Identificar cada ponto com o nome do ticker
- Linhas de referência no zero em ambos os eixos

**Entrega esperada:** Scatter com um ponto por ação identificado pelo ticker.

---

## 🌡️ 17 — Mapa de calor de correlação

**Objetivo:** Visualizar a matriz de correlação entre as ações de forma que facilite a identificação dos pares mais e menos correlacionados.

**Instruções:**
- Usar escala de cores divergente — vermelho para correlação negativa, azul para positiva
- Mostrar os valores numéricos dentro de cada célula
- Quanto mais intenso o azul, mais as ações se movem juntas

**Entrega esperada:** Heatmap com valores anotados e escala de cores correta.

---

## 🔵 18 — Scatterplot de correlação entre pares

**Objetivo:** Aprofundar a análise do par de ações com maior correlação identificado no heatmap.

**Por que usar o scatterplot após o heatmap?**
O heatmap mostra o número da correlação (ex: 0.87) mas não mostra como essa relação se comporta na prática.
O scatterplot coloca cada dia como um ponto — eixo X é o retorno de uma ação, eixo Y é o retorno da outra.
Com isso você vê se a relação é linear, se existem outliers e se a correlação se mantém em dias de alta volatilidade.

**Instruções:**
- Identificar automaticamente o par com maior correlação a partir da matriz da tarefa 11
- Cada ponto representa um dia de pregão
- Adicionar linha de tendência (regressão linear)
- Incluir o valor da correlação no título do gráfico
- Linhas de referência no zero em ambos os eixos

**Entrega esperada:** Scatterplot do par com maior correlação, com linha de tendência e valor de correlação no título.

> **Sequência analítica:** Tarefa 17 (heatmap) identifica os pares mais correlacionados → Tarefa 18 (scatterplot) aprofunda a análise do par mais relevante.

---

## 📊 19 — Análise de volume

**Objetivo:** Entender o comportamento do volume negociado e sua relação com o movimento de preços.

**O que o volume revela?**
Volume alto confirma um movimento de preço — se a ação sobe com volume alto, a tendência é mais confiável.
Volume baixo em uma alta pode indicar movimento fraco, sem convicção dos investidores.
É um dos indicadores mais usados para validar sinais de compra e venda.

**Instruções:**
- Gráfico de barras do volume diário por ação
- Calcular o volume médio diário por ticker e apresentar em tabela
- Identificar os 5 dias de maior volume de cada ação e verificar se coincidiram com grandes variações de preço

**Entrega esperada:** Gráfico de volume, tabela de volume médio e tabela dos 5 dias de maior volume com a variação de preço correspondente.

---

*MBA USP/ESALQ · Turma 261 · 2026*
