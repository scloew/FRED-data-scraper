#fred api data collection

#This project uses fredapi provided at
#https://github.com/mortada/fredapi

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


def collectDates(obs, op):

        dates=set(obs[list(obs.keys())[0]].keys()) #set of dates
        for o in obs.keys(): #loop collects set of all dates
            temp=set(obs[o].keys())
            dates=op(dates,temp)

        dates=sorted(dates)
        return dates

def fredapi(): #main loop


    print('running 2')

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
	
