import re



def search_all(x, text, flag=re.IGNORECASE):
    tmp = re.findall(x, text, flag)
    return tmp


def search_for_episodes(text):
    tmpset = set()
    tmp = search_all('S\d{2}E\d{2}', text)
    for i in tmp:
        tmpset.add(i.lower())
    tmpset = list(tmpset)
    tmpset.sort()
    return tmpset

def search_for_episodes(data):
    tmpset = set()
    tmp = search_all('S\d{2}E\d{2}', data)
    for i in tmp:
        tmpset.add(i.lower())
    tmpset = list(tmpset)
    tmpset.sort()
    return tmpset

# def search_for_movies(text):
#     dictmovies = dict()
#     tmp = search_all('<a href="/subtitles/[a-zA-Z0-9\-\"\>\s\:\(\)]+', text)
#     tmp = [i.replace('<a href="', '') for i in tmp]
#     for i in tmp:
#         t = i.split('\">')
#         try:
#             dictmovies[t[1]] = t[0]
#         except:
#             pass
#     return dictmovies


