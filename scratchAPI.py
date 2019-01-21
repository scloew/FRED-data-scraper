from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import re
import csv
import datetime
import operator

def getObs(seriesID): #records the observations for a given seriesID

    key="&api_key=3b7e7d31bcc6d28556c82c290eb3572e"
    obsUrl="https://api.stlouisfed.org/fred/series/observations?series_id="+seriesID+key
    obsHTML=urlopen(obsUrl)
    bsObj=BeautifulSoup(obsHTML,"html.parser")

    data=bsObj.prettify()
    temp=data.split("date=")

    l={}
    for i in range(1,len(temp)):
        start=temp[i].find("e=")
        stop=temp[i].find(">")
        l[temp[i][1:11]]=temp[i][start+3:stop-1]

    return l #returns dict{'date', value}


def searchTitle(): #takes search key and returns data sets from FED PDL
              #searches for observations for selected data sets

    url="https://fred.stlouisfed.org/search?st="+input("Enter search key: ")
    html=urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    table=bsObj.findAll("a", {"class":"series-title"})

    if table==[]:
        print("0 Results found")
        return {} #don't like multiple return statements
    else:
        print("\n 0) \n ALL")
        
    nameList=[]
    idList=[]
    index=0
    for entry in table:
        e=entry.prettify()
        start, stop=e.find(">")+1, e.find("</a>")-1
        nameList.append(e[start:stop]) #Get name
        start, stop=e.find("series/")+7, e.find(" style")-1
        idList.append(e[start:stop]) #series ID
        print(index+1, ')', nameList[index])
        index+=1

    choice="Enter choice(s): "

    vals={}
    choice=input("\n Enter choice(s): ")

    if choice=="0":
        choice=list(range(1,len(nameList)+1))
    else:
        choice=choice.split(' ')

    for c in choice:
        if ((isinstance(c, int) or c.isdigit()) and int(c) in range(1,len(nameList)+1)):
            vals[idList[int(c)-1]]=getObs(idList[int(c)-1])
        else:
            print("Invalid data selection:", c)

    return vals #returns dict of {'seriesID',getObs()}
    

def collectDates(obs, op):

        dates=set(obs[list(obs.keys())[0]].keys()) #set of dates
        for o in obs.keys(): #loop collects set of all dates
            temp=set(obs[o].keys())
            dates=op(dates,temp)

        dates=sorted(dates)
        return dates

def lucky(): #essentially works same as google's feeling lucky
             #takes first result from search for each search key
             #TODO Additional refactoring needed here?
    
    keys=input('Enter search keys: ').split(', ')
    print(keys)
    idList=[]
    obs={}
    
    for key in keys:
        url="https://fred.stlouisfed.org/search?st="+key
        html = urlopen(url)
        bsObj = BeautifulSoup(html, "html.parser")
        table = bsObj.findAll("a", {"class":"series-title"})
        if table==[]:
            print('0 results found for: ', key)
        else:
            e=table[0].prettify()
            start, stop=e.find("series/")+7, e.find(" style")-1
            idList.append(e[start:stop]) #series ID

    for i in idList:
        obs[i]=getObs(i)
    
    return obs

def fredScrape3(): #main loop

    print('running 1')

    obs, more={}, True
    if input('Feeling lucky? (Y/N): ').upper()=='Y':
        obs, more=lucky(), False
        
    while(more):
        obs.update(searchTitle())
        if input("Search Again(Y/N): ").upper() == 'N': #defaults to yes
            break

    if obs!={}: printCSV(obs)
    else: print('no data recorded -> good bye :)')

