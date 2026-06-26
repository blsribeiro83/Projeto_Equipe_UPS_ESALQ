from pathlib import Path
import re
import shutil
import unicodedata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def clear_outputs() -> None:
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_column(col: str) -> str:
    col = str(col).strip().lower()
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = re.sub(r"[^a-z0-9]+", "_", col).strip("_")
    return col


def parse_numeric(value):
    if pd.isna(value):
        return np.nan
    s = str(value).strip().replace("$", "").replace(",", "")
    s = s.replace("−", "-").replace("%", "")
    if s == "":
        return np.nan

    multiplier = 1.0
    if s.endswith("M"):
        multiplier = 1e6
        s = s[:-1]
    elif s.endswith("B"):
        multiplier = 1e9
        s = s[:-1]
    elif s.endswith("K"):
        multiplier = 1e3
        s = s[:-1]

    try:
        return float(s) * multiplier
    except ValueError:
        return np.nan


def task_01_carregar_dados() -> pd.DataFrame:
    frames = []
    for path in sorted(DATA_DIR.glob("*.csv")):
        df = pd.read_csv(path)
        if df.empty:
            continue
        df = df.rename(columns={c: normalize_column(c) for c in df.columns})
        df["ticker"] = path.stem
        frames.append(df)

    dados = pd.concat(frames, ignore_index=True)
    dados = dados.drop_duplicates().copy()
    return dados


def task_02_inspecao_inicial(dados: pd.DataFrame) -> dict:
    summary = {
        "shape": dados.shape,
        "dtypes": dados.dtypes.astype(str).to_dict(),
        "missing_values": dados.isna().sum().to_dict(),
        "head": dados.head(5).to_dict(orient="records"),
        "tail": dados.tail(5).to_dict(orient="records"),
        "describe": dados.describe(include="all").to_dict(),
    }

    markdown = [
        "# Inspeção inicial",
        "",
        f"- Shape: {summary['shape'][0]} linhas x {summary['shape'][1]} colunas",
        "- Tipos de dados:",
    ]
    for col, dtype in summary["dtypes"].items():
        markdown.append(f"  - {col}: {dtype}")
    markdown.extend(["- Valores ausentes:"])
    for col, value in summary["missing_values"].items():
        markdown.append(f"  - {col}: {value}")
    markdown.append("- Amostra inicial:")
    for row in summary["head"]:
        markdown.append(f"  - {row}")
    markdown.append("- Amostra final:")
    for row in summary["tail"]:
        markdown.append(f"  - {row}")

    (OUTPUT_DIR / "02_inspecao_inicial.md").write_text("\n".join(markdown), encoding="utf-8")
    return summary


def task_03_limpeza_dados(dados: pd.DataFrame) -> pd.DataFrame:
    dados = dados.copy()
    for col in ["price", "open", "high", "low", "vol", "change", "change_pct"]:
        if col in dados.columns:
            dados[col] = dados[col].apply(parse_numeric)

    dados = dados.dropna(subset=["price"]).drop_duplicates().copy()
    dados = dados.sort_values(["ticker", "date"]).reset_index(drop=True)
    dados.to_csv(OUTPUT_DIR / "03_dados_limpos.csv", index=False)
    return dados


def task_04_transformacoes(dados: pd.DataFrame) -> pd.DataFrame:
    dados = dados.copy()
    dados["date"] = pd.to_datetime(dados["date"], format="%m/%d/%Y", errors="coerce")
    dados = dados.dropna(subset=["date"]).copy()
    dados = dados.sort_values(["ticker", "date"]).reset_index(drop=True)
    dados["ano"] = dados["date"].dt.year
    dados["mes"] = dados["date"].dt.month
    dados = dados.set_index("date")
    dados = dados.sort_values(["ticker", "date"])
    dados.to_csv(OUTPUT_DIR / "04_dados_transformados.csv")
    return dados


def task_05_estatistica_descritiva(dados: pd.DataFrame) -> pd.DataFrame:
    resumo = (
        dados.groupby("ticker")["price"]
        .agg(["mean", "median", "std", "min", "max"])
        .round(4)
    )
    resumo.columns = ["media", "mediana", "desvio_padrao", "minimo", "maximo"]
    resumo.to_csv(OUTPUT_DIR / "05_resumo_estatistico.csv")
    return resumo


def task_06_retorno_diario(dados: pd.DataFrame) -> pd.DataFrame:
    dados["retorno_diario"] = dados.groupby("ticker")["price"].pct_change()
    dados[["retorno_diario"]].to_csv(OUTPUT_DIR / "06_retorno_diario.csv")
    return dados


def task_07_retorno_acumulado(dados: pd.DataFrame) -> pd.DataFrame:
    dados["retorno_acumulado"] = dados.groupby("ticker")["retorno_diario"].transform(
        lambda s: (1 + s.fillna(0)).cumprod()
    )
    dados[["retorno_acumulado"]].to_csv(OUTPUT_DIR / "07_retorno_acumulado.csv")
    return dados


def task_08_volatilidade_anualizada(dados: pd.DataFrame) -> pd.DataFrame:
    volatilidade = (
        dados.groupby("ticker")["retorno_diario"]
        .std(ddof=1)
        .mul(np.sqrt(252))
        .sort_values(ascending=False)
        .to_frame("volatilidade_anualizada")
    )
    volatilidade.to_csv(OUTPUT_DIR / "08_volatilidade_anualizada.csv")
    return volatilidade


def task_09_drawdown(dados: pd.DataFrame) -> pd.DataFrame:
    dados["pico_preco"] = dados.groupby("ticker")["price"].cummax()
    dados["drawdown"] = dados["price"] / dados["pico_preco"] - 1
    drawdown_max = (
        dados.groupby("ticker")["drawdown"]
        .min()
        .sort_values(ascending=True)
        .to_frame("drawdown_maximo")
    )
    drawdown_max.to_csv(OUTPUT_DIR / "09_drawdown_maximo.csv")
    return drawdown_max


def task_10_sharpe(dados: pd.DataFrame):
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
    return retorno_medio_anualizado, sharpe


def task_11_correlacao(dados: pd.DataFrame):
    retornos_pivot = (
        dados.reset_index()[["date", "ticker", "retorno_diario"]]
        .pivot(index="date", columns="ticker", values="retorno_diario")
    )
    correlacao = retornos_pivot.corr()
    correlacao.to_csv(OUTPUT_DIR / "11_correlacao_acoes.csv")
    return correlacao, retornos_pivot


def task_12_preco_medias_moveis(dados: pd.DataFrame) -> None:
    for ticker in dados["ticker"].unique():
        subset = dados[dados["ticker"] == ticker].copy()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(subset.index, subset["price"], label="Preço de fechamento", linewidth=1.2)
        ax.plot(subset.index, subset["price"].rolling(21).mean(), label="Média móvel 21 dias", linestyle="--")
        ax.plot(subset.index, subset["price"].rolling(200).mean(), label="Média móvel 200 dias", linestyle=":")
        ax.set_title(f"{ticker} — Preço e médias móveis")
        ax.set_xlabel("Data")
        ax.set_ylabel("Preço")
        ax.legend()
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"12_{ticker}_precos_medias_moveis.png", dpi=200)
        plt.close(fig)


def task_13_retorno_acumulado_plot(dados: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    for ticker, group in dados.groupby("ticker"):
        ax.plot(group.index, group["retorno_acumulado"], label=ticker)
    ax.axhline(1.0, linestyle="--", color="gray", linewidth=1)
    ax.set_title("Retorno acumulado das ações")
    ax.set_xlabel("Data")
    ax.set_ylabel("Retorno acumulado")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "13_retorno_acumulado_todas_acoes.png", dpi=200)
    plt.close(fig)


def task_14_histograma_retornos(dados: pd.DataFrame) -> None:
    for ticker in dados["ticker"].unique():
        subset = dados[dados["ticker"] == ticker]["retorno_diario"].dropna()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(subset, kde=True, ax=ax, bins=30)
        ax.axvline(0, linestyle="--", color="red")
        ax.set_title(f"{ticker} — Distribuição dos retornos diários")
        ax.set_xlabel("Retorno diário")
        ax.set_ylabel("Frequência")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"14_{ticker}_histograma_retornos.png", dpi=200)
        plt.close(fig)


def task_15_boxplot_retornos(dados: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=dados.reset_index(), x="ticker", y="retorno_diario", ax=ax)
    ax.set_title("Boxplot comparativo de retornos diários")
    ax.set_xlabel("Ticker")
    ax.set_ylabel("Retorno diário")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "15_boxplot_retornos.png", dpi=200)
    plt.close(fig)


def task_16_scatter_risco_retorno(volatilidade: pd.DataFrame, retorno_medio_anualizado: pd.DataFrame) -> None:
    scatter_df = pd.concat([volatilidade, retorno_medio_anualizado], axis=1).reset_index()
    scatter_df = scatter_df.rename(columns={"index": "ticker"})
    fig, ax = plt.subplots(figsize=(8, 5))
    for _, row in scatter_df.iterrows():
        ax.scatter(row["volatilidade_anualizada"], row["retorno_medio_anualizado"], s=80)
        ax.text(row["volatilidade_anualizada"], row["retorno_medio_anualizado"], row["ticker"], fontsize=9)
    ax.axhline(0, linestyle="--", color="gray")
    ax.axvline(0, linestyle="--", color="gray")
    ax.set_title("Retorno médio × Volatilidade anualizada")
    ax.set_xlabel("Volatilidade anualizada")
    ax.set_ylabel("Retorno médio anualizado")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "16_scatter_risco_retorno.png", dpi=200)
    plt.close(fig)


def task_17_heatmap_correlacao(correlacao: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Mapa de calor da correlação entre ações")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "17_heatmap_correlacao.png", dpi=200)
    plt.close(fig)


def task_18_scatter_par_correlacao(retornos_pivot: pd.DataFrame, correlacao: pd.DataFrame) -> None:
    upper = correlacao.where(np.triu(np.ones(correlacao.shape), k=1).astype(bool))
    pair = upper.stack().idxmax()
    ticker_x, ticker_y = pair
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(
        x=retornos_pivot[ticker_x],
        y=retornos_pivot[ticker_y],
        ax=ax,
        scatter_kws={"s": 8, "alpha": 0.5},
        line_kws={"color": "red"},
    )
    ax.axhline(0, linestyle="--", color="gray")
    ax.axvline(0, linestyle="--", color="gray")
    corr_value = correlacao.loc[ticker_x, ticker_y]
    ax.set_title(f"Correlação entre {ticker_x} e {ticker_y} (r = {corr_value:.2f})")
    ax.set_xlabel(ticker_x)
    ax.set_ylabel(ticker_y)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / f"18_scatter_{ticker_x}_{ticker_y}.png", dpi=200)
    plt.close(fig)


def task_19_analise_volume(dados: pd.DataFrame) -> None:
    for ticker in dados["ticker"].unique():
        subset = dados[dados["ticker"] == ticker].copy()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(
            subset.index,
            subset["vol"],
            color="#1f77b4",
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9,
        )
        ax.set_title(f"{ticker} — Volume diário")
        ax.set_xlabel("Data")
        ax.set_ylabel("Volume")
        fig.tight_layout()
        fig.savefig(OUTPUT_DIR / f"19_{ticker}_volume_diario.png", dpi=200)
        plt.close(fig)

    volume_medio = dados.groupby("ticker")["vol"].mean().sort_values(ascending=False).to_frame("volume_medio_diario")
    volume_medio.to_csv(OUTPUT_DIR / "19_volume_medio_diario.csv")

    top_volume = (
        dados.reset_index()[["date", "ticker", "vol", "price"]]
        .sort_values(["ticker", "vol"], ascending=[True, False])
        .groupby("ticker")
        .head(5)
        .copy()
    )
    top_volume["variacao_preco"] = top_volume.groupby("ticker")["price"].pct_change()
    top_volume.to_csv(OUTPUT_DIR / "19_top5_dias_maior_volume.csv", index=False)


def main() -> None:
    clear_outputs()
    
    dados = task_01_carregar_dados()
    task_02_inspecao_inicial(dados)
    dados = task_03_limpeza_dados(dados)
    dados = task_04_transformacoes(dados)
    resumo = task_05_estatistica_descritiva(dados)
    dados = task_06_retorno_diario(dados)
    dados = task_07_retorno_acumulado(dados)
    volatilidade = task_08_volatilidade_anualizada(dados)
    drawdown_max = task_09_drawdown(dados)
    retorno_medio_anualizado, sharpe = task_10_sharpe(dados)
    correlacao, retornos_pivot = task_11_correlacao(dados)
    
    task_12_preco_medias_moveis(dados)
    task_13_retorno_acumulado_plot(dados)
    task_14_histograma_retornos(dados)
    task_15_boxplot_retornos(dados)
    task_16_scatter_risco_retorno(volatilidade, retorno_medio_anualizado)
    task_17_heatmap_correlacao(correlacao)
    task_18_scatter_par_correlacao(retornos_pivot, correlacao)
    task_19_analise_volume(dados)
    
    print("Shape final do dataset:", dados.shape)
    print("\nResumo estatístico por ticker:")
    print(resumo)
    print("\nVolatilidade anualizada:")
    print(volatilidade)
    print("\nDrawdown máximo por ticker:")
    print(drawdown_max)
    print("\nRetorno médio anualizado:")
    print(retorno_medio_anualizado)
    print("\nÍndice de Sharpe:")
    print(sharpe)
    print("\nMatriz de correlação:")
    print(correlacao)
    print(f"\nArquivos gerados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
