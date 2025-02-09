import logging
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
from telegram.constants import ParseMode
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def admin_mention(update: Update, context) -> None:
    """Handle @admin mentions to notify all admins."""
    message_text = update.message.text.lower()
    if "@admin" in message_text:
        chat = update.effective_chat
        admins = await chat.get_administrators()
        admin_mentions = [f'<a href="tg://user?id={admin.user.id}">&#8205;</a>' for admin in admins if not admin.user.is_bot]
        
        await update.message.reply_text(
            "<code>All group admins have been alerted!</code>\n" + "".join(admin_mentions),
            parse_mode=ParseMode.HTML,
            reply_to_message_id=update.message.message_id
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(MessageHandler(filters.Regex(r"@admin"), admin_mention))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()