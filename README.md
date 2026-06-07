# 🎰 Bac Bo Analyzer Bot

Um bot inteligente para Telegram que analisa padrões e tendências do jogo Baccarat (Bac Bo).

## 🚀 Funcionalidades

- 📊 Análise de histórico de resultados
- 📈 Estatísticas e tendências
- 🔍 Detecção de padrões
- 💡 Recomendações baseadas em análise
- 📉 Gráficos e visualizações
- 💾 Armazenamento de dados
- 🎯 Rastreamento de sequências

## 📋 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Token de Bot do Telegram

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/tavinrodrigo844-png/bac-bo-analyzer.git
cd bac-bo-analyzer
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o token do bot:
```bash
cp config.example.py config.py
# Edite config.py com seu token
```

5. Execute o bot:
```bash
python main.py
```

## 🤖 Comandos do Bot

- `/start` - Inicia o bot
- `/analyze` - Analisa histórico de resultados
- `/stats` - Mostra estatísticas
- `/patterns` - Detecta padrões
- `/add_result` - Adiciona novo resultado
- `/history` - Mostra histórico
- `/reset` - Limpa o histórico
- `/help` - Mostra ajuda

## 📝 Exemplo de Uso

```
/add_result B
/add_result P
/add_result T
/analyze
```

## 🔧 Estrutura do Projeto

```
bac-bo-analyzer/
├── main.py              # Arquivo principal
├── bot.py               # Lógica do bot
├── analyzer.py          # Sistema de análise
├── database.py          # Gerenciamento de dados
├── config.py            # Configurações
├── requirements.txt     # Dependências
└── README.md           # Este arquivo
```

## 📚 Documentação

Veja [DOCS.md](DOCS.md) para documentação completa.

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.

## 📄 Licença

MIT License

## 👤 Autor

Tavin Rodrigo (@tavinrodrigo844-png)