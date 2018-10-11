#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardHide)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
import mySubscene
import my_telegram.telegram_movies
import my_telegram.telegram_series


user_dic = dict()
url = 'https://subscene.com/subtitles/title?q=%url%&l='
base_url = 'https://subscene.com'

FILMTYPE = 0

# Types
MOVIE = 1
SERIES = 2

# Series

SERIESNAME = 3
SEASON = 4
EPISODE = 5
SERIESRESULT = 6

# Movies

MOVIENAME = 7
NAMEORCHAPTERNUMBER = 8
MOVIEQUALITY = 9
MOVIERESOLUTION = 10


def start(bot, update):
    chat_id = update.message.chat_id
    try:
        del user_dic[chat_id]
    except:
        pass
    reply_keyboard = [['فیلم', 'سریال']]

    update.message.reply_text(
        '''
        سی دی . عکس . پاستور
        سی دی . سی دی
        ''',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return FILMTYPE


def film_type(bot, update):
    user = update.message.from_user
    message = update.message.text

    if message == 'سریال':
        update.message.reply_text('''
            دایی کدوم سریالو می خوای ؟
        ''',
                                  reply_markup=ReplyKeyboardHide())
        return SERIES

    elif message == 'فیلم':
        update.message.reply_text('''
             دایی کدوم فیلمو می خوای
        ''',
                                  reply_markup=ReplyKeyboardHide())
        return MOVIENAME


def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardHide())

    return ConversationHandler.END


def error(bot, update, error):
    return ConversationHandler.END


def add_message_to_dict(chat_id, message):
    if user_dic.get(chat_id) != None:
        tmp = user_dic.get(chat_id)
        tmp.append(message)
        user_dic[chat_id] = tmp
    else:
        user_dic[chat_id] = [message]


def end_conversation(bot, update):
    update.message.reply_text('Type /start again')
    return ConversationHandler.END


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("320891692:AAExGOwhTeEL27ZiDp5FZ3e8pXZxltc-f3Q")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FILMTYPE: [RegexHandler('^(فیلم|سریال)$', film_type)],

            SERIES: [MessageHandler(Filters.all, my_telegram.telegram_series.series)],

            SERIESNAME: [MessageHandler(Filters.all, my_telegram.telegram_series.series_name)],

            SEASON: [MessageHandler(Filters.all, my_telegram.telegram_series.season)],

            EPISODE: [MessageHandler(Filters.all, my_telegram.telegram_series.episode)],

            SERIESRESULT: [MessageHandler(Filters.all, my_telegram.telegram_series.series_result)],

            # movies

            MOVIENAME: [MessageHandler(Filters.all, my_telegram.telegram_movies.movie_name)],

            NAMEORCHAPTERNUMBER: [MessageHandler(Filters.all, my_telegram.telegram_movies.name_or_chapter_number)],

            MOVIEQUALITY: [MessageHandler(Filters.all, my_telegram.telegram_movies.movie_quality)],

            MOVIERESOLUTION: [MessageHandler(Filters.all, my_telegram.telegram_movies.movie_resolution)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
