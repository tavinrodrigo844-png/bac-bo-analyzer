"""
Bot handler for Bac Bo Analyzer
Manages all command handlers and interactions
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from database import Database
from analyzer import BaccaratAnalyzer


class BacBoBot:
    """Main bot handler class"""
    
    def __init__(self):
        self.db = Database("baccarat_data.db")
        self.analyzer = BaccaratAnalyzer(min_results=5)
        self.result_names = {'B': 'Banco', 'P': 'Jogador', 'T': 'Empate'}
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎰 **Bem-vindo ao Bac Bo Analyzer Bot!**

Este bot analisa padrões do jogo Baccarat e fornece insights sobre tendências.

**Como usar:**
• `/add_result B` - Adiciona resultado Banco
• `/add_result P` - Adiciona resultado Jogador
• `/add_result T` - Adiciona resultado Empate
• `/stats` - Mostra estatísticas
• `/patterns` - Detecta padrões
• `/analyze` - Análise completa
• `/predict` - Predição do próximo resultado
• `/history` - Mostra histórico
• `/reset` - Limpa dados
• `/help` - Mostra ajuda

Comece adicionando alguns resultados!
        """
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **Comandos Disponíveis:**

**Adicionar Resultados:**
• `/add_result B` - Banco ganhou
• `/add_result P` - Jogador ganhou
• `/add_result T` - Empate

**Análise:**
• `/stats` - Estatísticas gerais
• `/patterns` - Detecta padrões
• `/analyze` - Análise completa
• `/predict` - Próximo resultado previsto

**Gerenciamento:**
• `/history` - Últimos 20 resultados
• `/reset` - Limpa todos os dados
• `/help` - Este menu

**Dicas:**
Quanto mais resultados você adicionar, mais precisa será a análise!
Mínimo de 5 resultados para análise completa.
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def add_result_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /add_result command"""
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: `/add_result B` (ou P ou T)\n"
                "B = Banco, P = Jogador, T = Empate",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        result = context.args[0].upper()
        
        if result not in ['B', 'P', 'T']:
            await update.message.reply_text(
                "❌ Resultado inválido!\n"
                "Use: B (Banco), P (Jogador) ou T (Empate)"
            )
            return
        
        if self.db.add_result(result):
            result_name = self.result_names[result]
            stats = self.db.get_statistics()
            
            message = f"""
✅ **Resultado Adicionado!**

📊 Resultado: {result_name}

📈 **Totais:**
• Banco: {stats['banker']} ({stats['banker_percent']}%)
• Jogador: {stats['player']} ({stats['player_percent']}%)
• Empate: {stats['tie']} ({stats['tie_percent']}%)

Total: {stats['total']} resultados
            """
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("❌ Erro ao adicionar resultado")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        stats = self.db.get_statistics()
        
        if stats['total'] == 0:
            await update.message.reply_text(
                "📭 Nenhum resultado registrado ainda.\n"
                "Use `/add_result` para começar!",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        message = f"""
📊 **Estatísticas**

**Resultados Totais:** {stats['total']}

🏦 **Banco:**
   • Vezes: {stats['banker']}
   • Percentual: {stats['banker_percent']}%

👤 **Jogador:**
   • Vezes: {stats['player']}
   • Percentual: {stats['player_percent']}%

🤝 **Empate:**
   • Vezes: {stats['tie']}
   • Percentual: {stats['tie_percent']}%
        """
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def patterns_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /patterns command"""
        results = self.db.get_results()
        
        if len(results) < 5:
            await update.message.reply_text(
                "⚠️ Mínimo de 5 resultados necessários\n"
                f"Você tem: {len(results)}",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        patterns = self.analyzer.analyze_patterns(results)
        
        message = "🔍 **Padrões Detectados:**\n\n"
        
        # Alternating patterns
        if patterns['alternating']['found']:
            message += f"🔄 **Alternância:** {patterns['alternating']['count']} padrão(ões) encontrado(s)\n"
        
        # Repeating patterns
        if patterns['repeating']['found']:
            message += f"🔁 **Repetição:** {patterns['repeating']['count']} padrão(ões) encontrado(s)\n"
        
        # Streaks
        if patterns['streaks']['found']:
            message += f"📈 **Sequências:** {patterns['streaks']['count']} sequência(s) encontrada(s)\n"
            message += f"   Maior: {patterns['streaks']['longest']} resultados\n"
        
        # Pairs
        message += f"\n🔗 **Pares Mais Comuns:**\n"
        for pair_info in patterns['pairs']['most_common'][:3]:
            message += f"   • {pair_info['pair'][0]} → {pair_info['pair'][1]}: {pair_info['count']}x\n"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        results = self.db.get_results()
        
        if len(results) < 5:
            await update.message.reply_text(
                "⚠️ Mínimo de 5 resultados necessários para análise\n"
                f"Você tem: {len(results)}",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        message = self.analyzer.generate_recommendation(results)
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command"""
        results = self.db.get_results()
        
        if len(results) < 2:
            await update.message.reply_text(
                "⚠️ Mínimo de 2 resultados necessários\n"
                f"Você tem: {len(results)}",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        prediction = self.analyzer.predict_next(results)
        result_name = self.result_names[prediction['prediction']]
        
        message = f"""
🎯 **Predição do Próximo Resultado**

📌 **Previsão:** {result_name}
💡 **Razão:** {prediction['reason']}
📊 **Confiança:** {prediction['confidence']}%

⚠️ *Esta é apenas uma análise. Não há garantias em jogos de azar.*
        """
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /history command"""
        results = self.db.get_results(limit=20)
        
        if not results:
            await update.message.reply_text(
                "📭 Nenhum resultado registrado ainda"
            )
            return
        
        message = "📜 **Últimos Resultados:**\n\n"
        for i, result in enumerate(results, 1):
            result_name = self.result_names[result]
            message += f"{i}. {result_name}\n"
        
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command"""
        self.db.clear_results()
        await update.message.reply_text(
            "🔄 **Dados Limpos!**\n\n"
            "Todos os resultados foram removidos. Você pode começar do zero.",
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages for quick result addition"""
        text = update.message.text.upper()
        
        if text in ['B', 'P', 'T']:
            if self.db.add_result(text):
                result_name = self.result_names[text]
                await update.message.reply_text(f"✅ {result_name} adicionado!")
            else:
                await update.message.reply_text("❌ Erro ao adicionar")
        else:
            await update.message.reply_text(
                "📝 Envie apenas:\n"
                "• B - Banco\n"
                "• P - Jogador\n"
                "• T - Empate\n\n"
                "Ou use `/help` para mais comandos"
            )