# 📚 Documentação - Bac Bo Analyzer Bot

## Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso](#uso)
5. [Módulos](#módulos)
6. [API de Análise](#api-de-análise)

## Visão Geral

O **Bac Bo Analyzer Bot** é um bot para Telegram que fornece análise avançada do jogo Baccarat. Ele rastreia resultados, detecta padrões, calcula estatísticas e oferece previsões baseadas em análise de dados.

### Principais Características

- ✅ Rastreamento de resultados em tempo real
- ✅ Análise de padrões e tendências
- ✅ Cálculo de estatísticas
- ✅ Previsões inteligentes
- ✅ Histórico persistente
- ✅ Interface amigável via Telegram

## Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- Token de Bot do Telegram

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/tavinrodrigo844-png/bac-bo-analyzer.git
cd bac-bo-analyzer

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure o token
cp config.example.py config.py
# Edite config.py e adicione seu token
```

## Configuração

### Obter Token do Telegram Bot

1. Abra o Telegram
2. Procure por **@BotFather**
3. Use `/newbot` para criar um novo bot
4. Siga as instruções
5. Copie o token fornecido

### config.py

```python
# Token do seu bot
BOT_TOKEN = "seu_token_aqui"

# Arquivo de banco de dados
DATABASE_FILE = "baccarat_data.db"

# Configurações de análise
MIN_RESULTS_FOR_ANALYSIS = 5
PATTERN_WINDOW_SIZE = 10

# Configurações de gráficos
CHART_SIZE = (12, 6)
CHART_DPI = 100
```

## Uso

### Iniciando o Bot

```bash
python main.py
```

O bot será iniciado e estará pronto para receber comandos.

### Comandos Principais

#### Adicionar Resultados

```
/add_result B   # Banco ganhou
/add_result P   # Jogador ganhou
/add_result T   # Empate

Atalho: Digite apenas B, P ou T
```

#### Análise

```
/stats      # Mostra estatísticas gerais
/patterns   # Detecta padrões nos resultados
/analyze    # Análise completa e recomendações
/predict    # Predição do próximo resultado
```

#### Gerenciamento

```
/history    # Últimos 20 resultados
/reset      # Limpa todos os dados
/help       # Mostra menu de ajuda
/start      # Mostra mensagem de boas-vindas
```

### Exemplo de Uso

```
1. /add_result B   ✅ Banco adicionado
2. /add_result P   ✅ Jogador adicionado
3. /add_result B   ✅ Banco adicionado
4. /add_result B   ✅ Banco adicionado
5. /add_result P   ✅ Jogador adicionado
6. /stats          📊 Mostra: 3 Banco (60%), 2 Jogador (40%)
7. /patterns       🔍 Detecta padrões
8. /predict        🎯 Próximo resultado previsto
```

## Módulos

### database.py

Gerencia persistência de dados usando JSON.

**Principais Funções:**

```python
db = Database("baccarat_data.db")

# Adicionar resultado
db.add_result('B')

# Obter resultados
results = db.get_results()
results = db.get_results(limit=20)

# Estatísticas
stats = db.get_statistics()

# Limpar dados
db.clear_results()
```

### analyzer.py

Realiza análise de padrões e previsões.

**Principais Funções:**

```python
analyzer = BaccaratAnalyzer(min_results=5)

# Analisar padrões
patterns = analyzer.analyze_patterns(results)

# Predizer próximo resultado
prediction = analyzer.predict_next(results)

# Obter estatísticas
stats = analyzer.get_statistics(results)

# Gerar recomendação
rec = analyzer.generate_recommendation(results)
```

### bot.py

Handler de comandos do Telegram.

**Principais Métodos:**

- `start_command()` - Boas-vindas
- `add_result_command()` - Adicionar resultado
- `stats_command()` - Mostrar stats
- `patterns_command()` - Detectar padrões
- `analyze_command()` - Análise completa
- `predict_command()` - Previsão
- `history_command()` - Histórico
- `reset_command()` - Limpar dados

### main.py

Arquivo principal que inicia o bot.

```bash
python main.py
```

## API de Análise

### Padrões Detectados

#### 1. Alternância
Detecta sequências alternadas (B-P-B-P ou similar)

```python
patterns = analyzer.analyze_patterns(results)
alternating = patterns['alternating']
# {
#   'found': True/False,
#   'sequences': [...],
#   'count': número
# }
```

#### 2. Repetição
Detecta padrões que se repetem

```python
repeating = patterns['repeating']
# {
#   'found': True/False,
#   'patterns': [...],
#   'count': número
# }
```

#### 3. Sequências (Streaks)
Detecta resultados consecutivos iguais

```python
streaks = patterns['streaks']
# {
#   'found': True/False,
#   'streaks': [
#     {'result': 'Banco', 'count': 3},
#     ...
#   ],
#   'longest': 3
# }
```

#### 4. Pares
Detecta pares mais comuns

```python
pairs = patterns['pairs']
# {
#   'total_pairs': número,
#   'unique_pairs': número,
#   'most_common': [
#     {'pair': ['Banco', 'Jogador'], 'count': 5},
#     ...
#   ]
# }
```

### Estrutura de Resultados

Resultados são armazenados com timestamps:

```python
{
  "result": "B",  # B, P, ou T
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## Troubleshooting

### Bot não responde

1. Verifique se o token está correto em `config.py`
2. Verifique conexão com internet
3. Reinicie o bot: `python main.py`

### Erro de banco de dados

1. Delete o arquivo `baccarat_data.db`
2. Reinicie o bot (recriará o banco)

### Erro de importação

```bash
pip install --upgrade -r requirements.txt
```

## Licença

MIT License - veja LICENSE.md para detalhes

## Suporte

Para problemas ou sugestões, abra uma issue no GitHub.