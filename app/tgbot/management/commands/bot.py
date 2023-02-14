import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, filters
from tgbot.handlers.commands import *
class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    def handle(self, *args, **options):
        app = ApplicationBuilder().token(settings.TOKEN).build()

        start_handler = CommandHandler('start', start)
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('cut', selection_shortening_mode)],
            states={
                SELECT_SHORTENING_MODE: [
                    # MessageHandler(filters.Regex("^(Only link|Link & QR)$"), wait_url)
                    CallbackQueryHandler(wait_url, pattern="^(Only link|Link & QR)$"),
                    CallbackQueryHandler(cancel, pattern="^cancel$"),
                ],
                WAIT_URL: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cut_link)
                ],
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        app.add_handler(start_handler)
        app.add_handler(conv_handler)

        app.run_polling()
