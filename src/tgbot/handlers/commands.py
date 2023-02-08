from django.conf import settings
from django.core.exceptions import ValidationError
from telegram import Update
from telegram.ext import ContextTypes
from ugc.shortener import Shortener
from ugc.models import Profile


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)
    text = "I'm a bot, please talk to me!"
    await context.bot.send_message(chat_id=chat_id, text=text)

async def cut(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    chat_id = update.effective_chat.id
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)
    try:
        link = await Shortener(user).cut_link(args[0])
        text = settings.HOST + '/' + link.token
        await context.bot.send_message(chat_id=chat_id, text=text)
    except (ValidationError, IndexError):
        await context.bot.send_message(chat_id=chat_id,
                                       text='Your URL is incorrect. Please, send the correct URL address.')
