#!/usr/bin/env python
# coding: utf-8

# # Análise de ações com Python
# 
# Este notebook acompanha as tarefas 01 a 19 do projeto em ordem, seguindo exatamente a estrutura descrita em TASKS.
# 
# - Bloco 1: coleta, inspeção e limpeza dos dados
# - Bloco 2: análise estatística e medidas de risco
# - Bloco 3: visualizações comparativas

# In[ Carregar Módulos ]:

from pathlib import Path
import shutil
import re
import unicodedata
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use('Agg')
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style='whitegrid')

DATA_DIR = Path('data/raw')
OUTPUT_DIR = Path('outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

# Limpeza da pasta de outputs antes de gerar os artefatos
for item in OUTPUT_DIR.iterdir():
    if item.is_dir():
        shutil.rmtree(item)
    else:
        item.unlink()
OUTPUT_DIR.mkdir(exist_ok=True)


# In[ Bloco 1: coleta, inspeção e limpeza dos dados ]:

# In[ Tarefa 01 — Carregamento dos dados ]:

# Leitura e consolidação dos arquivos CSV em um único DataFrame com a coluna ticker
def normalize_column(col: str) -> str:
    col = str(col).strip().lower()
    col = unicodedata.normalize('NFKD', col).encode('ascii', 'ignore').decode('utf-8')
    col = re.sub(r'[^a-z0-9]+', '_', col).strip('_')
    return col

def parse_numeric(value):
    if pd.isna(value):
        return np.nan
    s = str(value).strip().replace('$', '').replace(',', '')
    s = s.replace('−', '-').replace('%', '')
    if s == '':
        return np.nan

    multiplier = 1.0
    if s.endswith('M'):
        multiplier = 1e6
        s = s[:-1]
    elif s.endswith('B'):
        multiplier = 1e9
        s = s[:-1]
    elif s.endswith('K'):
        multiplier = 1e3
        s = s[:-1]

    try:
        return float(s) * multiplier
    except ValueError:
        return np.nan

frames = []
for path in sorted(DATA_DIR.glob('*.csv')):
    df = pd.read_csv(path)
    if df.empty:
        continue
    df = df.rename(columns={c: normalize_column(c) for c in df.columns})
    df['ticker'] = path.stem
    frames.append(df)

dados = pd.concat(frames, ignore_index=True)
dados = dados.drop_duplicates().copy()
dados.head()


# In[ Tarefa 02 — Inspeção inicial ]:

# Resumo do dataset: linhas, colunas, tipos de dados, valores ausentes, primeiras e últimas linhas, e estatísticas básicas.

print('Shape:', dados.shape)
print('Tipos de dados:')
print(dados.dtypes)
print('Valores ausentes:')
print(dados.isna().sum())
print('Primeiras linhas:')
print(dados.head())
print('Últimas linhas:')
print(dados.tail())
print('Resumo estatístico:')
print(dados.describe())


# In[ Tarefa 03 — Limpeza dos dados ]:

for col in ['price', 'open', 'high', 'low', 'vol', 'change', 'change_pct']:
    if col in dados.columns:
        dados[col] = dados[col].apply(parse_numeric)

dados = dados.dropna(subset=['price']).drop_duplicates().copy()
dados = dados.sort_values(['ticker', 'date']).reset_index(drop=True)
dados.head()


# In[ Bloco 1 — Coleta e Tratamento ]:


# In[ Tarefa 04 — Transformações ]:
# Converter a coluna de data para datetime, ordenar, extrair ano e mês, e preparar o índice temporal.

dados = dados.copy()
dados['date'] = pd.to_datetime(dados['date'], format='%m/%d/%Y', errors='coerce')
dados = dados.dropna(subset=['date']).copy()
dados = dados.sort_values(['ticker', 'date']).reset_index(drop=True)
dados['ano'] = dados['date'].dt.year
dados['mes'] = dados['date'].dt.month
dados = dados.set_index('date')
dados = dados.sort_values(['ticker', 'date'])
dados.head()


# In[ Tarefa 05 — Análise estatística descritiva ]:

resumo = (
    dados.groupby('ticker')['price']
    .agg(['mean', 'median', 'std', 'min', 'max'])
    .round(4)
)
resumo.columns = ['media', 'mediana', 'desvio_padrao', 'minimo', 'maximo']
resumo


# In[ Tarefa 06 — Retorno diário ]:

dados['retorno_diario'] = dados.groupby('ticker')['price'].pct_change()
dados[['retorno_diario']].head()


# In[ Tarefa 07 — Retorno acumulado ]:

dados['retorno_acumulado'] = dados.groupby('ticker')['retorno_diario'].transform(lambda s: (1 + s.fillna(0)).cumprod())
dados[['retorno_acumulado']].head()


# In[ Tarefa 08 — Volatilidade anualizada ]:

volatilidade = (
    dados.groupby('ticker')['retorno_diario']
    .std(ddof=1)
    .mul(np.sqrt(252))
    .sort_values(ascending=False)
    .to_frame('volatilidade_anualizada')
)
volatilidade


# In[ Tarefa 09 — Drawdown ]:

dados['pico_preco'] = dados.groupby('ticker')['price'].cummax()
dados['drawdown'] = dados['price'] / dados['pico_preco'] - 1
drawdown_max = (
    dados.groupby('ticker')['drawdown']
    .min()
    .sort_values(ascending=True)
    .to_frame('drawdown_maximo')
)
drawdown_max

# In[ Tarefa 10 — Índice de Sharpe ]:

retorno_medio = dados.groupby("ticker")["retorno_diario"].mean()
desvio = dados.groupby("ticker")["retorno_diario"].std(ddof=1)
retorno_medio_anualizado = (retorno_medio * np.sqrt(252)).to_frame("retorno_medio_anualizado")
sharpe = (
    (retorno_medio / desvio * np.sqrt(252))
    .replace([np.inf, -np.inf], np.nan)
    .dropna()
    .sort_values(ascending=False)
    .to_frame("sharpe_anualizado")
)
retorno_medio_anualizado.to_csv(OUTPUT_DIR / "10_retorno_medio_anualizado.csv")
sharpe.to_csv(OUTPUT_DIR / "10_sharpe_anualizado.csv")


# In[ Tarefa 11 — Correlação entre ações ]:

retornos_pivot = (
    dados.reset_index()[['date', 'ticker', 'retorno_diario']]
    .pivot(index='date', columns='ticker', values='retorno_diario')
)
correlacao = retornos_pivot.corr()
correlacao


# In[ Tarefa 12 — Gráfico de preços e médias móveis ]:

for ticker in dados['ticker'].unique():
    subset = dados[dados['ticker'] == ticker].copy()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(subset.index, subset['price'], label='Preço de fechamento', linewidth=1.2)
    ax.plot(subset.index, subset['price'].rolling(21).mean(), label='Média móvel 21 dias', linestyle='--')
    ax.plot(subset.index, subset['price'].rolling(200).mean(), label='Média móvel 200 dias', linestyle=':')
    ax.set_title(f'{ticker} — Preço e médias móveis')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço')
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f'12_{ticker}_precos_medias_moveis.png', dpi=200)
    plt.close(fig)


# In[ Tarefa 13 — Gráfico de retorno acumulado ]:

fig, ax = plt.subplots(figsize=(10, 5))
for ticker, group in dados.groupby('ticker'):
    ax.plot(group.index, group['retorno_acumulado'], label=ticker)
ax.axhline(1.0, linestyle='--', color='gray', linewidth=1)
ax.set_title('Retorno acumulado das ações')
ax.set_xlabel('Data')
ax.set_ylabel('Retorno acumulado')
ax.legend()
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '13_retorno_acumulado_todas_acoes.png', dpi=200)
plt.close(fig)


# In[ Tarefa 14 — Histograma de retornos diários ]:

for ticker in dados['ticker'].unique():
    subset = dados[dados['ticker'] == ticker]['retorno_diario'].dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(subset, kde=True, ax=ax, bins=30)
    ax.axvline(0, linestyle='--', color='red')
    ax.set_title(f'{ticker} — Distribuição dos retornos diários')
    ax.set_xlabel('Retorno diário')
    ax.set_ylabel('Frequência')
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f'14_{ticker}_histograma_retornos.png', dpi=200)
    plt.close(fig)


# In[ Tarefa 15 — Boxplot comparativo de retornos ]:

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=dados.reset_index(), x='ticker', y='retorno_diario', ax=ax)
ax.set_title('Boxplot comparativo de retornos diários')
ax.set_xlabel('Ticker')
ax.set_ylabel('Retorno diário')
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '15_boxplot_retornos.png', dpi=200)
plt.close(fig)


# In[ Tarefa 16 — Scatter retorno médio × volatilidade ]:

scatter_df = pd.concat([volatilidade, retorno_medio_anualizado], axis=1).reset_index()
scatter_df = scatter_df.rename(columns={'index': 'ticker'})
fig, ax = plt.subplots(figsize=(8, 5))
for _, row in scatter_df.iterrows():
    ax.scatter(row['volatilidade_anualizada'], row['retorno_medio_anualizado'], s=80)
    ax.text(row['volatilidade_anualizada'], row['retorno_medio_anualizado'], row['ticker'], fontsize=9)
ax.axhline(0, linestyle='--', color='gray')
ax.axvline(0, linestyle='--', color='gray')
ax.set_title('Retorno médio × Volatilidade anualizada')
ax.set_xlabel('Volatilidade anualizada')
ax.set_ylabel('Retorno médio anualizado')
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '16_scatter_risco_retorno.png', dpi=200)
plt.close(fig)


# In[ Tarefa 17 — Mapa de calor de correlação ]:

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlacao, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
ax.set_title('Mapa de calor da correlação entre ações')
fig.tight_layout()
fig.savefig(OUTPUT_DIR / '17_heatmap_correlacao.png', dpi=200)
plt.close(fig)


# In[ Tarefa 18 — Scatterplot de correlação entre pares ]:

upper = correlacao.where(np.triu(np.ones(correlacao.shape), k=1).astype(bool))
pair = upper.stack().idxmax()
ticker_x, ticker_y = pair
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(x=retornos_pivot[ticker_x], y=retornos_pivot[ticker_y], ax=ax, scatter_kws={'s': 8, 'alpha': 0.5}, line_kws={'color': 'red'})
ax.axhline(0, linestyle='--', color='gray')
ax.axvline(0, linestyle='--', color='gray')
corr_value = correlacao.loc[ticker_x, ticker_y]
ax.set_title(f'Correlação entre {ticker_x} e {ticker_y} (r = {corr_value:.2f})')
ax.set_xlabel(ticker_x)
ax.set_ylabel(ticker_y)
fig.tight_layout()
fig.savefig(OUTPUT_DIR / f'18_scatter_{ticker_x}_{ticker_y}.png', dpi=200)
plt.close(fig)


# In[ Tarefa 19 — Análise de volume ]:

for ticker in dados['ticker'].unique():
    subset = dados[dados['ticker'] == ticker].copy()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(
        subset.index,
        subset['vol'],
        color='#1f77b4',
        edgecolor='black',
        linewidth=0.8,
        alpha=0.9,
    )
    ax.set_title(f'{ticker} — Volume diário')
    ax.set_xlabel('Data')
    ax.set_ylabel('Volume')
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f'19_{ticker}_volume_diario.png', dpi=200)
    plt.close(fig)

volume_medio = dados.groupby('ticker')['vol'].mean().sort_values(ascending=False).to_frame('volume_medio_diario')
volume_medio


# In[ Tarefa 19 — Top 5 dias de maior volume ]:

top_volume = (
    dados.reset_index()[['date', 'ticker', 'vol', 'price']]
    .sort_values(['ticker', 'vol'], ascending=[True, False])
    .groupby('ticker')
    .head(5)
    .copy()
)
top_volume['variacao_preco'] = top_volume.groupby('ticker')['price'].pct_change()
top_volume

