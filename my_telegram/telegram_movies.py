#!/usr/bin/env python
# -*- coding: utf-8 -*-

import my_telegram.telegramBot
import mySubscene
import get_from_url


def movie_name(bot, update):
    moviename = update.message.text
    if moviename == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    chat_id = update.message.chat_id

    tmp = get_from_url.get_list(my_telegram.telegramBot.url.replace('%url%', moviename), 'Popular')
    message = 'Choose : \r\n'
    counter = 0
    for key, value in tmp.items():
        message += '\r\n /' + str(counter) + ' ' + str(key)
        counter += 1

    update.message.reply_text(message)
    my_telegram.telegramBot.add_message_to_dict(chat_id, tmp)
    return my_telegram.telegramBot.NAMEORCHAPTERNUMBER


def name_or_chapter_number(bot, update):
    chat_id = update.message.chat_id

    moviename = update.message.text
    if moviename == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    moviename = moviename[1:]

    tmp = my_telegram.telegramBot.user_dic.get(chat_id)
    tmpdict = tmp[-1]
    i = 0
    for key, value in tmpdict.items():
        if str(i) == str(moviename):
            moviename = value
            break
        i += 1
    my_telegram.telegramBot.user_dic[chat_id] = [moviename]
    update.message.reply_text('''
        quality :
            example :
                Bluray
                DvdRip
    ''')
    return my_telegram.telegramBot.MOVIEQUALITY


def movie_quality(bot, update):
    moviequality = update.message.text
    if moviequality == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    moviequality = str(moviequality).strip()
    chat_id = update.message.chat_id
    update.message.reply_text('''
        resolution :
            example :
                720
                1080
    ''')
    my_telegram.telegramBot.add_message_to_dict(chat_id, moviequality)

    return my_telegram.telegramBot.MOVIERESOLUTION


def movie_resolution(bot, update):

    movieresolution = update.message.text
    if movieresolution == '/start':
        return my_telegram.telegramBot.end_conversation(bot, update)
    movieresolution = str(movieresolution).strip()
    chat_id = update.message.chat_id
    my_telegram.telegramBot.add_message_to_dict(chat_id, movieresolution)

    tmp = my_telegram.telegramBot.user_dic.get(chat_id)
    url = my_telegram.telegramBot.base_url + tmp[0]
    filters = []
    for i in range(1, len(tmp)):
        filters.append(tmp[i])
    strurls = mySubscene.get_subtitle_urls(url, filters)
    if strurls == 'null':
        update.message.reply_text(strurls)
        del my_telegram.telegramBot.user_dic[chat_id]
        return my_telegram.telegramBot.ConversationHandler.END

    link = mySubscene.get_download_link(strurls)
    update.message.reply_text(link)
    del my_telegram.telegramBot.user_dic[chat_id]
    return my_telegram.telegramBot.ConversationHandler.END