#fred api data collection

from fredapi import Fred
from urllib.request import urlopen
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import operator
import json
import re
import csv

fred=Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e')

def searchTitle(*args): #searches for items matching search key
                        #returns list of responses
        
        if not args: searchKey=input("Enter search key: ")
        else: searchKey=args[0]
        df=fred.search(searchKey).T
        titles=df.columns.values.tolist()
        l=['']
        if not args: print('0) ALL')
        index=1
        for t in titles:
                temp=df[t].values.tolist()
                l.append((temp[12],t))
                if args: break
                print(index,')',l[index][0])
                index+=1
                if index==51: break

        return l #returns list of tuples (series title, series id)


def getObs(l, *args): #takes list from search and returns dict with observations

    if not args:
            sels=input('Enter selection: ')
            sels=sels.split(' ')
            if '0' in sels: sels=range(1,len(l))
    else: sels=[1]

    obs={} #dict{'seriesID': {'date':value}}
        
    for i in sels:
        try:
                res=fred.get_series_latest_release(l[int(i)][1])
                obs[l[int(i)][1]]=dict(zip(res.keys(),res.values.tolist()))
        except:
                print('Invalid data selection: ', i)

    return obs #return dict{series ID, {date, value}}


def lucky(): #works like google's feeling lucky
        
    keys=input('Enter search keys: ').split(', ')
    idList, obs=[], {}

    for key in keys:
        try: obs.update(getObs(searchTitle(key),key))
        except: print('Search error: ', key)

    return obs
    


def writeMeta(l, fname):

    mname=fname[:fname.rfind('.')]+'Meta.txt'
    print('writing to: ', mname)

    with open(mname, 'w') as file:
        file.write('Accessed ' + str(datetime.date.today())+'\n'+'\n'+'\n')
        for ID in l:
            key="&api_key=3b7e7d31bcc6d28556c82c290eb3572e&file_type=json"
            url='https://api.stlouisfed.org/fred/series?series_id='+ID+key
            response=urlopen(url)
            content=response.read()
            data=json.loads(content.decode('utf8'))
            file.write(ID+'\n')
            file.write(data['seriess'][0]['title']+'\n')
            file.write(data['seriess'][0]['seasonal_adjustment']+ '\n'+ 'frequency: '+ data['seriess'][0]['frequency']+' units: '+ data['seriess'][0]['units']+'\n')
            file.write('start: '+ data['seriess'][0]['observation_start']+ ' end:'+ data['seriess'][0]['observation_end']+'\n \n ---------------- \n ---------------- \n')
        file.close()

def collectDates(obs, op):

        dates=set(obs[list(obs.keys())[0]].keys()) #set of dates
        for o in obs.keys(): #loop collects set of all dates
            temp=set(obs[o].keys())
            dates=op(dates,temp)

        dates=sorted(dates)
        return dates      

def printCSV(obs):

    print('Would you like to record for all dates (A) or all compatible dates (C)?')
    if input().upper()=='C': op=operator.and_
    else: op=operator.or_

    fileName=input("Enter file name to write to: ")
    with open(fileName, "w") as file: #should have option for append (swithc?)
        wr=csv.writer(file)

        keys=["dates"]
        for k in obs.keys(): keys.append(k)
        wr.writerow(keys)

        dates=collectDates(obs, op)
        if dates==[] and op==operator.and_:
                print("No compatible dates; recording all dates.")
                dates=collectDates(obs, operator.or_)

        for d in dates:
            l=[str(d)[:10]]
            for k in range(1,len(keys)):
                if d not in obs[keys[k]].keys():
                    l.append('.')
                else:
                    l.append(obs[keys[k]][d])
            wr.writerow(l)

        if input('Would you like to record meta data?(Y/N): ').upper()=='Y':
            writeMeta(list(obs.keys()), fileName)#defaults to no

def fredapi(): #main loop


    obs, more={}, True
    if input('Feeling lucky? (Y/N): ').upper()=='Y':
        obs, more=lucky(), False
        
    while(more):
        try:
                obs.update(getObs(searchTitle()))
        except:
                print('search error')
        if input("Search Again(Y/N): ").upper() == 'N':
            break

    if obs!={}: printCSV(obs)
    else: print('No data recorded -> good bye :)')
	
