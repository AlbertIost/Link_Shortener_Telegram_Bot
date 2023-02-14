from django.core.exceptions import ValidationError
from telegram import Update, MenuButtonDefault, MenuButtonCommands, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from ugc.shortener import Shortener
from ugc.models import Profile
from tgbot.utils import get_qrcode, get_short_url

WAIT_URL, SELECT_SHORTENING_MODE = range(2)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = "Commands list:\n" \
           "/start - restart bot\n" \
           "/cut - shorten the link\n" \
           "/help - get commands list"
    await context.bot.send_message(chat_id=chat_id, text=text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text='Link shortening canceled')
    query = update.callback_query
    if query is not None:
        await query.delete_message()
    return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)
    text = "I'm a bot that can shorten the link. Type /help for get commands list."
    await context.bot.send_message(chat_id=chat_id, text=text)


async def selection_shortening_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Only link", callback_data='Only link'),
            InlineKeyboardButton("Link & QR", callback_data='Link & QR'),
        ],
        [
            InlineKeyboardButton("Cancel", callback_data='cancel'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "I want to know what you want to get:\n"
        "only a shortened link or also a QR-code.\n\n",
        reply_markup=reply_markup)

    return SELECT_SHORTENING_MODE


async def wait_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.effective_chat.id
    query = update.callback_query
    await query.answer()
    context.chat_data['selected_mode'] = query.data
    await query.edit_message_text(text=f'Selected mode: {query.data}.\n'
                                       f'Please, send the URL that you want to shorten.\n\n'
                                       f'Send /cancel to cancel link shortening.')

    return WAIT_URL


async def cut_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user, created = await Profile.objects.aget_or_create(external_id=chat_id)

    try:
        link = await Shortener(user).cut_link(update.message.text)
        short_url = get_short_url(link)
        if context.chat_data.get('selected_mode') == 'Only link':
            await context.bot.send_message(chat_id=chat_id, text=short_url)
        elif context.chat_data['selected_mode'] == 'Link & QR':
            await context.bot.send_photo(chat_id=chat_id, photo=get_qrcode(short_url), caption=short_url)

        context.chat_data.clear()
        return ConversationHandler.END

    except (ValidationError, IndexError):
        await context.bot.send_message(chat_id=chat_id,
                                       text='Your URL is incorrect. Please, send the correct URL address.')
        return WAIT_URL
