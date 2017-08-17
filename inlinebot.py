#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from uuid import uuid4

import re

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineQueryResultPhoto
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Load json
tagDict = {}
def load_json():
    import json

    with open('data.json', 'r', encoding='UTF-8') as f:
        data=json.load(f)

    for img in data:
        for patt in img['pattern']:
                pre_url = []
                if patt in tagDict:
                    pre_url = tagDict[patt]
                pre_url.append(img['url'])
                tagDict[patt] = pre_url

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('想跟人起爭議嗎？找"圖戰機器人"吧！\n使用方法：\n@IMwarbot 黑人問號\n\n按 /help 獲得更多資訊！')
    bot.send_photo(chat_id=update.message.chat_id, photo='http://i.imgur.com/0yEJDZJ.jpg')

def help(bot, update):
    update.message.reply_text('本機器人收錄近期知名梗圖,內容包含：\n鸚鵡兄弟\n鎖鏈康妮\n靠北工程師\nHTTP貓\n..')

def list(bot, update):
    pic_list = []
    for pat, urls in tagDict.items():
        pic_list.append(pat)
    li = ' '.join(pic_list)
    update.message.reply_text(li)

def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Caps",
                                            input_message_content=InputTextMessageContent(
                                                query.upper())))

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Bold",
                                            input_message_content=InputTextMessageContent(
                                                "*%s*" % escape_markdown(query),
                                                parse_mode=ParseMode.MARKDOWN)))

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Italic",
                                            input_message_content=InputTextMessageContent(
                                                "_%s_" % escape_markdown(query),
                                                parse_mode=ParseMode.MARKDOWN)))

    results.append(InlineQueryResultPhoto(id=uuid4(),
        title = "???",
        photo_url = 'http://i.imgur.com/2NIcsCB.jpg',
        thumb_url = 'http://i.imgur.com/2NIcsCB.jpg'))

    update.inline_query.answer(results)

import random
def echo(bot, update):
    txt = update.message.text
    for pat, urls in tagDict.items():
        if re.search(pat, txt):
            bot.send_photo(chat_id=update.message.chat_id, photo=random.choice(urls))
            break

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    # Read token from file
    import os.path
    TOKEN = ''
    token_file = "token.txt"
    if os.path.isfile(token_file):
        f = open(token_file, 'r')
        TOKEN = f.read()
        if TOKEN:
            TOKEN = TOKEN.rstrip()
    if not TOKEN:
        TOKEN = input("Please input your bot token: ")

    # Load json
    load_json()

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", list))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    from telegram.ext import MessageHandler, Filters
    echo_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(echo_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
