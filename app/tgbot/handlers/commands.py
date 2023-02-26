import datetime
import logging
import sys
import traceback

from asgiref.sync import sync_to_async, async_to_sync
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import close_old_connections
from django.db.utils import OperationalError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from telegram.helpers import mention_html

from ugc.shortener import Shortener
from ugc.models import Profile, Link, ClickOnLink, ProfileLevel
from tgbot.utils import get_qrcode, get_short_url

WAIT_URL, SELECT_SHORTENING_MODE = range(2)

logging.basicConfig(
    filename='bot_logs/errors.log',
    format='%(asctime)s - %(name)s - %(levelname)s\n%(message)s',
    level=logging.ERROR
)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    devs = settings.DEVS_ID.split(',')

    if update.effective_message:
        text = "Unfortunately, an error occurred while processing the message. " \
               "We are already working on this problem."
        await update.effective_message.reply_text(text)

    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = []
    if update.effective_user:
        bad_user = mention_html(
            update.effective_user.id,
            f'{update.effective_user.first_name} {update.effective_user.last_name}'
        )
        payload.append(f' с пользователем {bad_user}')

    text = f"Ошибка <code>{context.error}</code> случилась{''.join(payload)}"

    for dev_id in devs:
        await context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)

    raise


async def devs_notification(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    devs = settings.DEVS_ID.split(',')
    for dev in devs:
        await context.bot.send_message(chat_id=dev, text=message, parse_mode=ParseMode.HTML)


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

@sync_to_async
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        user, created = Profile.objects.get_or_create(external_id=chat_id,
                                                      defaults={
                                                          'profile_level': ProfileLevel.get_default_level()
                                                      })
    except OperationalError:
        close_old_connections()
        user, created = Profile.objects.get_or_create(external_id=chat_id,
                                                      defaults={
                                                          'profile_level': ProfileLevel.get_default_level()
                                                      })

    # notification developers about new user
    if created:
        user_href = mention_html(
            chat_id,
            f'{update.effective_user.first_name} {update.effective_user.last_name}'
        )
        async_to_sync(devs_notification)(update, context, f'Новый пользователь: {user_href}')

    text = "I'm a bot that can shorten the link. Type /help for get commands list."
    async_to_sync(context.bot.send_message)(chat_id=chat_id, text=text)


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


@sync_to_async
def cut_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        try:
            user = Profile.objects.get(external_id=chat_id)
        except OperationalError:
            close_old_connections()
            user = Profile.objects.get(external_id=chat_id)

        try:
            link = Shortener(user).cut_link(update.message.text)
        except OperationalError:
            close_old_connections()
            link = Shortener(user).cut_link(update.message.text)

        short_url = get_short_url(link)

        if context.chat_data.get('selected_mode') == 'Only link':
            async_to_sync(context.bot.send_message)(chat_id=chat_id, text=short_url)

        elif context.chat_data['selected_mode'] == 'Link & QR':
            async_to_sync(context.bot.send_photo)(chat_id=chat_id, photo=get_qrcode(short_url), caption=short_url)

        user_href = mention_html(
            chat_id,
            f'{update.effective_user.first_name} {update.effective_user.last_name}'
        )

        async_to_sync(devs_notification)(update, context, f'Пользователь: {user_href}.\n'
                                                 f'Сократил ссылку: {link.original_link}\n'
                                                 f'Получил результат: {short_url}')
        context.chat_data.clear()
        return ConversationHandler.END

    except (ValidationError, IndexError):
        async_to_sync(context.bot.send_message)(chat_id=chat_id,
                                       text='Your URL is incorrect. Please, send the correct URL address.')
        return WAIT_URL


@sync_to_async
def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        user_links = Link.objects.filter(profile__external_id=chat_id)
    except OperationalError:
        close_old_connections()
        user_links = Link.objects.filter(profile__external_id=chat_id)

    for link in user_links:
        clicks_counter = ClickOnLink.objects.filter(link=link).count()
        clicks_counter_today = ClickOnLink.objects.filter(link=link,
                                                          click_at__gte=datetime.date.today()).count()
        async_to_sync(context.bot.send_message)(chat_id=chat_id,
                                                text=f'By the link {link.original_link} '
                                                     f'clicked {clicks_counter} times\n'
                                                     f'Today: {clicks_counter_today}')