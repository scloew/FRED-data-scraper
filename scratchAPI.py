from urllib.request import urlopen
from bs4 import BeautifulSoup

key = '&api_key=3b7e7d31bcc6d28556c82c290eb3572e'


def search_title(search_key, lucky = False) :
    """
    searches for items matching searchKey
     returning a list of returning list of tuple(datetimet, series id)
    :param search_key:
    :param lucky:
    :return:
    """
    url = "https://fred.stlouisfed.org/search?st=" + search_key
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, "html.parser")
    table = bs_obj.findAll("a", {"class" : "series-title"})

    series = []
    for entry in table :
        e = entry.prettify()
        start, stop = e.find(">") + 1, e.find("</a>") - 1
        series_title = (e[start :stop])
        start, stop = e.find("series/") + 7, e.find(" style") - 1
        series_id = (e[start :stop])
        series.append((series_title, series_id))
        if lucky :
            break
    return series


def get_obs(series_ID) :
    """returns dict{series ID: {date:value}"""
    obs_url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_ID}{key}'
    obs_html = urlopen(obs_url)
    bs_obj = BeautifulSoup(obs_html, 'html.parser')

    data = bs_obj.prettify()
    temp = data.split("date=")

    d = {}
    for i in range(1, len(temp)) :
        start = temp[i].find("e=")
        stop = temp[i].find(">")
        d[temp[i][1 :11]] = temp[i][start + 3 :stop - 1]

    return {series_ID : d}
