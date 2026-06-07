# Configuration file for Bac Bo Analyzer Bot
# Copy this to config.py and fill in your values

# Telegram Bot Token
# Get it from @BotFather on Telegram
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Database configuration
DATABASE_FILE = "baccarat_data.db"

# Analysis settings
MIN_RESULTS_FOR_ANALYSIS = 5
PATTERN_WINDOW_SIZE = 10

# Chart settings
CHART_SIZE = (12, 6)
CHART_DPI = 100

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "bot.log"

# Features
ENABLE_CHARTS = True
ENABLE_PATTERNS = True
ENABLE_RECOMMENDATIONS = True