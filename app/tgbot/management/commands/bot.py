import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler, \
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
        help_handler = CommandHandler('help', help)
        statistics_handler = CommandHandler('statistics', statistics)
        list_handler = CommandHandler('list', list)
        cut_link_conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('cut', check_number_of_links)],
            states={
                SELECT_SHORTENING_MODE: [
                    CallbackQueryHandler(wait_url, pattern="^(Only link|Link & QR)$"),
                    CallbackQueryHandler(cancel, pattern="^cancel$"),
                ],
                WAIT_URL: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cut_link)
                ]

            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
        delete_link_conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('delete', choose_links_for_delete)],
            states={
                CHOOSE_LINK_FOR_DELETE: [
                    CallbackQueryHandler(delete_link, pattern="^[0-9]+$"),
                    CallbackQueryHandler(cancel, pattern="^cancel$"),
                ]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )

        app.add_handler(start_handler)
        app.add_handler(help_handler)
        app.add_handler(cut_link_conversation_handler)
        app.add_handler(delete_link_conversation_handler)
        app.add_handler(statistics_handler)
        app.add_handler(list_handler)
        app.add_error_handler(error_handler)

        app.run_polling()
