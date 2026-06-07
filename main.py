"""
Main Bot File for Bac Bo Analyzer
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import BOT_TOKEN
from bot import BacBoBot

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = BacBoBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await bot.start_command(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await bot.help_command(update, context)


async def add_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /add_result command"""
    await bot.add_result_command(update, context)


async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /analyze command"""
    await bot.analyze_command(update, context)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    await bot.stats_command(update, context)


async def patterns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /patterns command"""
    await bot.patterns_command(update, context)


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /history command"""
    await bot.history_command(update, context)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command"""
    await bot.reset_command(update, context)


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /predict command"""
    await bot.predict_command(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages (quick add results)"""
    await bot.handle_message(update, context)


def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_result", add_result))
    application.add_handler(CommandHandler("analyze", analyze))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("patterns", patterns))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("predict", predict))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()