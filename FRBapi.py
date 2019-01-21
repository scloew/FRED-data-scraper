#FRB api for net centric final project

#does compatible dates work :: nan values recorded - should I check for nan's?

#This project uses FRB api provided at
#https://github.com/avelkoski/FRB

from fred import Fred
from urllib.request import urlopen
import operator
import re
import csv
import datetime
import json
fr = Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e',response_type='dict')

def printOptions

def searchTitle(searchKey, lucky=False): #finds series titles @TODO refactor this; not single purpose (i.e use helpers)
                                                              @TODO better naming skills

    ##PRINT options
    ##collect selections
    ##collect observations
    ##return observations
    params={'limit':50}
    res=fr.series.search(str(searchKey),params=params)
    if res==[]:
        print('No results found for ', searchKey)
        return []
    
    index=1
    l=['']
    if not lucky: print('0: ALL')
    for item in res:
        l.append((item['title'],item['id']))
        if lucky: break
        print(index,item['title'])
        index+=1



    return l #returns list of tuples (series title, series id)

def getObs(l, lucky=False): #takes list from searchTitle and gets obs #TODO implement lucky

    if l == []: return {} #TODO don't like safety check here; put in driver
    sels=input('Enter selection: ')
    sels=sels.split(' ')
    if '0' in sels: sels=range(1,len(l))
    params = {
         'limit':10000,
         'output_type':1
         }

    obs={} 
        
    for i in sels:
        try:
            res=fr.series.observations(l[int(i)][1],params=params)
            tempD={}
            for j in res:
                temp=str(j['date'])
                tempD[temp[0:10]]=j['value']
            obs[l[int(i)][1]]=tempD
        except:
            print('Invalid data selection: ', i)

    return obs #returns dict{'seriesID': {'date':value}}

def collectDates(obs, op):

        dates=set(obs[list(obs.keys())[0]].keys()) #set of dates
        for o in obs.keys(): #loop collects set of all dates
            temp=set(obs[o].keys())
            dates=op(dates,temp)

        dates=sorted(dates)
        return dates

def FRBapi(): #main loop

    print('running 1')

    obs, more={}, True
    if input('Feeling lucky? (Y/N): ').upper()=='Y':
        obs, more = lucky(), False
        
    while(more):
        try:
            obs.update(getObs(searchTitle()))
            if input("Search Again(Y/N): ").upper()=="N":
                break
        except: print('Err')

    if obs!={}: printCSV(obs)
    else: print('No data recorded -> good bye :)')
