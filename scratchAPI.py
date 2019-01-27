from urllib.request import urlopen
from bs4 import BeautifulSoup

key="&api_key=3b7e7d31bcc6d28556c82c290eb3572e"

def searchTitle(searchKey, lucky=False):

    url="https://fred.stlouisfed.org/search?st="+searchKey
    html=urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    table=bsObj.findAll("a", {"class" : "series-title"})

    series = []
    for entry in table:
        e=entry.prettify()
        start, stop=e.find(">")+1, e.find("</a>")-1
        title = (e[start:stop]) #series title
        start, stop = e.find("series/")+7, e.find(" style")-1
        id = (e[start:stop]) #series ID
        series.append((title, id))
        if(lucky): break

    return series


def getObs(seriesID):

    obsUrl="https://api.stlouisfed.org/fred/series/observations?series_id="+seriesID+key
    obsHTML=urlopen(obsUrl)
    bsObj=BeautifulSoup(obsHTML,"html.parser")

    data=bsObj.prettify()
    temp=data.split("date=")

    d={}
    for i in range(1,len(temp)):
        start=temp[i].find("e=")
        stop=temp[i].find(">")
        d[temp[i][1:11]]=temp[i][start+3:stop-1]

    return {seriesID : d}
    #return dict{series ID, {date, value}}
