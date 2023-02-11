import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
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
        cut_handler = CommandHandler('cut', cut)

        app.add_handler(start_handler)
        app.add_handler(cut_handler)

        app.run_polling()
