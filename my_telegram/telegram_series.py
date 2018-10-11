#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import (ConversationHandler)
import mySubscene
import my_telegram.telegramBot
import get_from_url


def series(bot, update):
    seriesname = update.message.text
    if seriesname == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    chat_id = update.message.chat_id
    tmp = get_from_url.get_list(my_telegram.telegramBot.url.replace('%url%', seriesname), 'TV-Series')
    message = 'Choose : \r\n'
    counter = 0
    for key, value in tmp.items():
        message += '\r\n /' + str(counter) + ' ' + str(key)
        counter += 1
    update.message.reply_text(message)
    my_telegram.telegramBot.add_message_to_dict(chat_id, tmp)
    return my_telegram.telegramBot.SERIESNAME


def series_name(bot, update):
    seasonnumber = update.message.text
    if seasonnumber == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    seasonnumber = seasonnumber[1:]
    chat_id = update.message.chat_id

    tmp = my_telegram.telegramBot.user_dic.get(chat_id)
    tmpdict = tmp[-1]
    i = 0
    for key, value in tmpdict.items():
        if str(i) == str(seasonnumber):
            seasonnumber = value
            break
        i += 1
    my_telegram.telegramBot.user_dic[chat_id] = [seasonnumber]
    my_telegram.telegramBot.add_message_to_dict(chat_id, seasonnumber)

    persian_subtitles = mySubscene.get_persian_subtitles(my_telegram.telegramBot.base_url + seasonnumber)
    my_telegram.telegramBot.user_dic[chat_id] = [persian_subtitles]
    subtitle_list = mySubscene.get_series_subtitle_list(persian_subtitles)
    message = 'Choose : '

    for i in subtitle_list:
        message += '\r\n /' + i

    update.message.reply_text(message)
    return my_telegram.telegramBot.SEASON


def season(bot, update):
    episodenumber = update.message.text
    if episodenumber == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    episodenumber = episodenumber.strip()[1:]
    chat_id = update.message.chat_id
    update.message.reply_text('''
    Quality:
        example :
        bluray
        dvdrip
    ''')
    my_telegram.telegramBot.add_message_to_dict(chat_id, episodenumber)
    return my_telegram.telegramBot.EPISODE

def episode(bot, update):
    quality = update.message.text
    if quality == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    chat_id = update.message.chat_id
    user = update.message.from_user
    update.message.reply_text('''
        Resolution :
        example :
        720
        1080
    ''')
    my_telegram.telegramBot.add_message_to_dict(chat_id, quality)
    return my_telegram.telegramBot.SERIESRESULT

def series_result(bot, update):
    resolution = update.message.text
    if resolution == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    resolution = resolution.strip()
    chat_id = update.message.chat_id
    my_telegram.telegramBot.add_message_to_dict(chat_id, resolution)

    tmp = my_telegram.telegramBot.user_dic.get(chat_id)

    filters = []
    for i in range(1, len(tmp)):
        filters.append(tmp[i])
    strurls = mySubscene.get_series_subtitle_urls(my_telegram.telegramBot.base_url, tmp, filters)
    link = mySubscene.get_download_link(strurls)
    update.message.reply_text(link)
    del my_telegram.telegramBot.user_dic[chat_id]
    return my_telegram.telegramBot.ConversationHandler.END