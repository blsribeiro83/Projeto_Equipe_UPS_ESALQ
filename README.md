# 📊 Projeto Equipe — MBA Data Science, IA & Analytics

### USP/ESALQ | Turma 261 | 2026

Projeto colaborativo de análise de dados financeiros desenvolvido pelos alunos do MBA USP/ESALQ.
A ideia é aplicar progressivamente o que aprendemos no curso: tratamento de dados, estatística, visualização, web scraping, APIs e machine learning.

-----

## 🗂️ Estrutura do repositório

```
Projeto_Equipe_UPS_ESALQ/
│
├── data/
│   └── raw/          ← datasets brutos (ninguém edita esses arquivos)
│
├── bruno/            ← pasta individual de cada membro
├── igor/
├── paulo/
├── wagner/
│   └── ...
│
├── requirements.txt  ← bibliotecas Python necessárias
└── README.md         ← este arquivo
```

> Cada membro trabalha **apenas dentro da própria pasta**. Nunca edite a pasta de outra pessoa.

-----

## 🚀 Como entrar no projeto (faça isso uma única vez)

### 1. Aceite o convite

Você vai receber um e-mail do GitHub com o convite para colaborar.
Clique em **Accept invitation**.

### 2. Instale o Git

Baixe em: <https://git-scm.com/download/win>
Instale com as opções padrão (clique Next em tudo).

Após instalar, abra o **Prompt de Comando** (tecla Windows → digite `cmd` → Enter) e configure seu nome:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
```

> Use o mesmo e-mail da sua conta GitHub.

### 3. Clone o repositório

No terminal, navegue até onde quer salvar o projeto e execute:

```bash
git clone https://github.com/blsribeiro83/Projeto_Equipe_UPS_ESALQ.git
cd Projeto_Equipe_UPS_ESALQ
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Crie sua branch com seu nome

```bash
git checkout -b seunome
git push origin seunome
```

Exemplo: `git checkout -b igor`

### 6. Crie sua pasta pessoal

```bash
mkdir seunome
echo "# Seu Nome" > seunome/README.md
```

Pronto — seu ambiente está configurado.

-----

## 📋 Workflow diário (repita sempre que trabalhar no projeto)

```bash
# 1. Garanta que está na sua branch (não na main)
git branch

# 2. Baixe as atualizações mais recentes
git pull origin main

# 3. Abra o JupyterLab
jupyter lab

# 4. Trabalhe normalmente nos seus notebooks...

# 5. Ao terminar, salve e suba seu trabalho
git add seunome/
git commit -m "feat: descrição do que você fez"
git push origin seunome
```

> ⚠️ **Nunca use `git add .`** — isso adiciona arquivos de todos, não só os seus.
> Use sempre `git add seunome/` com o seu nome.

-----

## 🔀 Como submeter seu trabalho para a main (Pull Request)

Quando quiser que seu trabalho entre na versão oficial do projeto:

1. Acesse o repositório em github.com
1. Clique em **Pull requests → New pull request**
1. Selecione: **base: main ← compare: suabranch**
1. Preencha o título e descrição do que você fez
1. Clique em **Create pull request**
1. Avise no grupo para alguém revisar e aprovar

> Ninguém faz merge do próprio PR — sempre peça para um colega revisar.

-----

## ✍️ Convenção de mensagens de commit

Use o formato: `tipo: descrição curta do que foi feito`

|Tipo   |Quando usar                                     |
|-------|------------------------------------------------|
|`feat:`|Adicionou algo novo (notebook, análise, gráfico)|
|`fix:` |Corrigiu um erro                                |
|`docs:`|Atualizou documentação ou README                |
|`data:`|Adicionou ou atualizou dados                    |

**Exemplos:**

```
feat: análise exploratória PETR4 com boxplot
fix: corrige encoding UTF-8 na leitura do CSV
data: adiciona histórico IBOV 2022-2024
docs: atualiza README com instruções de setup
```

-----

## 📦 Bibliotecas do projeto

|Biblioteca  |Para que serve                                |
|------------|----------------------------------------------|
|`pandas`    |Manipulação e análise de dados                |
|`numpy`     |Cálculos numéricos                            |
|`matplotlib`|Gráficos                                      |
|`seaborn`   |Gráficos estatísticos                         |
|`openpyxl`  |Leitura de arquivos Excel                     |
|`yfinance`  |Download de dados financeiros via API (fase 2)|

-----

## ❓ Dúvidas frequentes

**Errei algo e quero desfazer antes de commitar:**

```bash
git checkout -- seunome/arquivo.ipynb
```

**Quero ver o que mudou antes de commitar:**

```bash
git status
git diff
```

**Esqueci em qual branch estou:**

```bash
git branch
```

**Quero mudar de branch:**

```bash
git checkout seunome
```

-----

## 👥 Membros da equipe

|Nome             |Branch      |GitHub       |
|-----------------|------------|-------------|
|Bruno Ribeiro    |`bruno`     |@blsribeiro83|
|Igor Milhomens   |`igor`      |—            |
|Paulo            |`paulo`     |—            |
|Wagner Bortoletto|`wagner`    |—            |
|Mayara Silva     |`mayara`    |—            |
|Carolina Soares  |`carolina`  |—            |
|Gleycielle       |`gleycielle`|—            |


> Atualize esta tabela com seu username do GitHub quando entrar no projeto.

-----

## 📚 Recursos de apoio

- [Manual Git & GitHub — PDF do projeto](data/raw/) *(em breve)*
- [Documentação oficial do Git](https://git-scm.com/doc)
- [GitHub Docs em português](https://docs.github.com/pt)

-----

*MBA USP/ESALQ · Turma 261 · 2026*
