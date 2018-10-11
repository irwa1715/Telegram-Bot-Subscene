import regex
import get_from_url
import my_telegram.telegramBot


class SubsceneData:
    url = None
    pageTitle = None


def get_subtitle_urls(url, filters):
    l = get_persian_subtitles(url)
    result = []
    try:
        for index, value in enumerate(l):
            counter = 0
            f = value.pageTitle
            for k in filters:
                if k.lower() in str(f).lower():
                    counter += 1
                    continue
                else:
                    break
            if counter == len(filters):
                result.append(value)
    except Exception as e:
        print(e)
    print(result)
    if len(result) == 0:
        return 'null'
    else:
        return result


def get_series_subtitle_urls(base_url, url, filters):
    result = []
    print(1)
    try:
        for index, value in enumerate(url[0]):
            counter = 0
            f = str(value.pageTitle)
            f = f.lower()
            for k in filters:
                if k.lower() in f:
                    counter += 1
                    continue
                else:
                    break
            if counter == len(filters):
                result.append(value)
    except Exception as e:
        pass
    if len(result) == 0:
        return 'null'
    else:
        return result


def get_series_subtitle_list(data):
    lst = []
    for i in data:
        lst.append(i.pageTitle)
    lst = ''.join(lst)
    tmpset = regex.search_for_episodes(lst)
    return tmpset


def get_download_link(urls):

    soup = get_from_url.get_soup(my_telegram.telegramBot.base_url+urls[0].url)

    link = soup.find('div', {'class': 'download'}).a.get('href')
    link = str(my_telegram.telegramBot.base_url) + str(link)
    return link


def get_persian_subtitles(url):
    soup = get_from_url.get_soup(url)
    html = soup.find_all('td', {'class' : 'a1'})
    lst_subtitles = list()
    for i in html:
        if 'farsi_persian' in i.a.get('href').lower():
            s = SubsceneData()
            s.url = str(i.a.get('href')).strip()
            s.pageTitle = str(i.a.span.findNext('span').text).strip()
            lst_subtitles.append(s)
    return lst_subtitles




