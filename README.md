# 📊 Projeto Equipe — MBA Data Science, IA & Analytics
### USP/ESALQ | Turma 261 | 2026

Projeto colaborativo de análise de dados financeiros desenvolvido pelos alunos do MBA USP/ESALQ.
Aplicamos progressivamente o que aprendemos no curso: tratamento de dados, estatística descritiva e visualização.

---

## 🎯 O que este projeto faz

A partir de dados históricos de ações brasileiras baixados do Yahoo Finance, este projeto realiza:

1. **Coleta** — leitura de arquivos CSV/XLSX com histórico de preços de múltiplas ações
2. **Tratamento** — limpeza, padronização e consolidação dos dados com pandas
3. **Análise estatística** — medidas de posição, dispersão, retornos diários e correlação entre ações
4. **Visualização** — gráficos de evolução de preços, distribuição de retornos, boxplots e mapa de calor

> As tarefas detalhadas de cada etapa estão no arquivo **[TASKS.md](TASKS.md)**.
> Cada tarefa tem objetivo, instruções e referência de código.

---

## 🗂️ Estrutura do repositório

```
Projeto_Equipe_UPS_ESALQ/
│
├── data/
│   └── raw/                    ← datasets brutos (não edite estes arquivos)
│       └── acoes_yahoo.csv     ← histórico de preços das ações
│
├── notebook_base.ipynb         ← notebook principal com a estrutura do projeto
├── requirements.txt            ← bibliotecas Python necessárias
├── TASKS.md                    ← tarefas detalhadas com instruções de código
└── README.md                   ← este arquivo
```

---

## 🚀 Como participar do projeto

O projeto usa o modelo de **fork** — cada pessoa cria uma cópia independente do repositório
na própria conta do GitHub, desenvolve lá, e submete o trabalho via Pull Request.

Você não precisa ser convidado. Basta ter uma conta no GitHub.

---

### Passo 1 — Instale o Git

Baixe em: **https://git-scm.com/download/win**

Instale com as opções padrão (clique Next em todas as telas).

Após instalar, abra o **Prompt de Comando**:
- Pressione a tecla **Windows**
- Digite **cmd**
- Pressione **Enter**

Configure sua identidade com os comandos abaixo.
Digite cada linha e pressione Enter:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@exemplo.com"
```

> Use o mesmo e-mail da sua conta GitHub.

---

### Passo 2 — Faça o fork do repositório

**O que é um fork?**
Fork é uma cópia completa deste repositório que fica na **sua própria conta** do GitHub.
Você trabalha na sua cópia com total liberdade, sem afetar o repositório central.

**Como fazer:**
1. Acesse este repositório no GitHub
2. Clique no botão **Fork** (canto superior direito da página)
3. Clique em **Create fork**

Pronto — agora você tem uma cópia em:
`https://github.com/seunome/Projeto_Equipe_UPS_ESALQ`

---

### Passo 3 — Clone o seu fork

> Clone o **seu fork**, não o repositório original.

Abra o Prompt de Comando e navegue até a pasta onde quer salvar o projeto:

```bash
cd Documentos
```

Depois execute o clone substituindo `seunome` pelo seu username do GitHub:

```bash
git clone https://github.com/seunome/Projeto_Equipe_UPS_ESALQ.git
```

Entre na pasta do projeto:

```bash
cd Projeto_Equipe_UPS_ESALQ
```

---

### Passo 4 — Instale as dependências

Com o terminal ainda aberto dentro da pasta do projeto, execute:

```bash
pip install -r requirements.txt
```

Aguarde a instalação terminar. Isso instala todas as bibliotecas necessárias (pandas, numpy, matplotlib, seaborn, etc).

---

### Passo 5 — Abra o JupyterLab

**O que é o JupyterLab?**
É o ambiente onde você vai escrever e executar o código Python.
Funciona no navegador (Chrome, Firefox, Edge) mas roda localmente no seu computador.

**Como abrir:**

No terminal, dentro da pasta do projeto, execute:

```bash
jupyter lab
```

O JupyterLab vai abrir automaticamente no seu navegador.
Se não abrir, copie o endereço que aparecer no terminal (começa com `http://localhost:8888`) e cole no navegador.

**Navegando no JupyterLab:**
- Na barra lateral esquerda você verá a estrutura de pastas do projeto
- Clique duas vezes em `notebook_base.ipynb` para abrir o notebook
- Cada bloco cinza é uma célula de código — clique nela e pressione **Shift + Enter** para executar

**Para encerrar o JupyterLab:**
- Feche a aba do navegador
- No terminal, pressione **Ctrl + C** e confirme com **S** ou **Y**

---

## 📋 Workflow diário — como salvar e enviar seu trabalho

Este é o ciclo que você vai repetir toda vez que trabalhar no projeto.

### 1. Antes de começar — atualize seu fork

```bash
git pull upstream main
```

> Isso garante que você está trabalhando com a versão mais recente do projeto.
> Na primeira vez, pode ser necessário conectar ao repositório original:
> ```bash
> git remote add upstream https://github.com/blsribeiro83/Projeto_Equipe_UPS_ESALQ.git
> ```

### 2. Trabalhe no JupyterLab

Abra o JupyterLab, edite o notebook, salve com **Ctrl + S**.

### 3. Verifique o que foi alterado

Antes de commitar, veja quais arquivos você modificou:

```bash
git status
```

O terminal vai mostrar uma lista de arquivos em vermelho (modificados) e verde (prontos para commit).

### 4. Adicione os arquivos ao commit

**O que é "adicionar ao commit"?**
Antes de salvar no Git, você precisa dizer quais arquivos quer incluir.
É como selecionar itens antes de colocar na caixa.

```bash
git add .
```

> O ponto (`.`) adiciona todos os arquivos modificados.
> Rode `git status` novamente — agora os arquivos aparecem em verde.

### 5. Faça o commit

**O que é um commit?**
É um ponto de salvamento permanente no histórico do projeto.
Cada commit tem uma mensagem descrevendo o que foi feito.

```bash
git commit -m "feat: descrição do que você fez"
```

**Exemplos de boas mensagens:**
```
git commit -m "feat: análise exploratória PETR4 com boxplot"
git commit -m "fix: corrige leitura do CSV com encoding utf-8"
git commit -m "feat: mapa de calor de correlação entre ações"
```

> A mensagem deve descrever **o que** foi feito, não **como**.
> Evite mensagens genéricas como "update", "mudanças" ou "arrumei".

### 6. Envie para o GitHub

```bash
git push origin main
```

Seu trabalho agora está salvo no seu fork no GitHub.

---

## 🔀 Como submeter seu trabalho (Pull Request)

Quando quiser contribuir com seu trabalho para o projeto central:

1. Acesse **seu fork** no GitHub (`github.com/seunome/Projeto_Equipe_UPS_ESALQ`)
2. Clique em **Contribute → Open pull request**
3. Verifique que está indo de **seu fork → repositório original**
4. Preencha o título e descreva o que você desenvolveu
5. Clique em **Create pull request**
6. Avise no grupo para que alguém revise e aprove

> O repositório central só recebe trabalho aprovado via Pull Request.
> Ninguém faz merge do próprio PR — sempre peça para um colega revisar.

---

## 📦 Bibliotecas utilizadas

| Biblioteca | Para que serve |
|---|---|
| `pandas` | Manipulação e análise de dados |
| `numpy` | Cálculos numéricos |
| `matplotlib` | Gráficos |
| `seaborn` | Gráficos estatísticos |
| `openpyxl` | Leitura de arquivos Excel |
| `yfinance` | Download de dados financeiros via API (fase 2) |

---

## ❓ Dúvidas frequentes

**O JupyterLab não abre no navegador:**
Copie o endereço que aparece no terminal (ex: `http://localhost:8888/lab?token=...`) e cole manualmente no navegador.

**Como vejo o histórico de commits:**
```bash
git log --oneline
```

**Como desfaço uma alteração antes de commitar:**
```bash
git checkout -- nome_do_arquivo.ipynb
```

**Esqueci de atualizar antes de começar e agora tem conflito:**
Avise no grupo — alguém pode ajudar a resolver.

---

## 👥 Membros da equipe

| Nome | GitHub |
|------|--------|
| Bruno Ribeiro | @blsribeiro83 |
| Igor Milhomens | — |
| Paulo | — |
| Wagner Bortoletto | — |
| Mayara Silva | — |
| Carolina Soares | — |
| Gleycielle | — |

> Atualize esta tabela com seu username do GitHub ao entrar no projeto.

---

## 📚 Recursos de apoio

- **[TASKS.md](TASKS.md)** — tarefas detalhadas com instruções e código
- [Documentação oficial do Git](https://git-scm.com/doc)
- [GitHub Docs em português](https://docs.github.com/pt)
- [Yahoo Finance](https://finance.yahoo.com) — fonte dos dados

---

*MBA USP/ESALQ · Turma 261 · 2026*
