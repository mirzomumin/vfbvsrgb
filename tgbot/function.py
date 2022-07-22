#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

from .models import Post

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    posts = Post.objects.filter(title__contains=query)

    results = [
        InlineQueryResultArticle(
            id=post.id,
            title=post.title,
            url=post.image,
            thumb_url=post.image,
            thumb_width=3,
            thumb_height=3,
            input_message_content=InputTextMessageContent(f'{post.title}\n {post.text}'),
        ) for post in posts
    ]

    update.inline_query.answer(results)