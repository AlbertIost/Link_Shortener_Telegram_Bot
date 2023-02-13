from django.core.exceptions import ValidationError
from telegram import Update, MenuButtonDefault, MenuButtonCommands
from telegram.ext import ContextTypes, ConversationHandler
from ugc.shortener import Shortener
from ugc.models import Profile
from tgbot.utils import get_qrcode, get_short_url

WAIT_URL = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.set_chat_menu_button(chat_id=chat_id, menu_button=MenuButtonCommands())
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)
    text = "I'm a bot, please talk to me!"
    await context.bot.send_message(chat_id=chat_id, text=text)


async def wait_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id,
                                   text='Please, send the URL that you want to shorten.')
    return WAIT_URL


async def cut_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)

    try:
        link = await Shortener(user).cut_link(update.message.text)
        short_url = get_short_url(link)
        await context.bot.send_photo(chat_id=chat_id, photo=get_qrcode(short_url), caption=short_url)
        return ConversationHandler.END

    except (ValidationError, IndexError):
        await context.bot.send_message(chat_id=chat_id,
                                       text='Your URL is incorrect. Please, send the correct URL address.')
        return WAIT_URL
