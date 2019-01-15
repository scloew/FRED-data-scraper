#FRB api for net centric final project

#does compatible dates work :: nan values recorded - should I check for nan's?

from fred import Fred
from urllib.request import urlopen
import operator
import re
import csv
import datetime
import json
fr = Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e',response_type='dict')

def searchTitle(*args): #finds series titles

    if not args: searchKey=input('Enter search key: ')
    else: searchKey=args[0]
    params={'limit':50}
    res=fr.series.search(str(searchKey),params=params)
    if res==[]:
        print('No results found for ', searchKey)
        return []
    
    index=1
    l=['']
    if not args: print('0: ALL')
    for item in res:
        l.append((item['title'],item['id']))
        if args: break
        print(index,item['title'])
        index+=1

    return l #returns list of tuples (series title, series id)

def getObs(l, *args): #takes list from searchTitle and gets obs

    if l == []: return {}
    if not args:
        sels=input('Enter selection: ')
        sels=sels.split(' ')
        if '0' in sels: sels=range(1,len(l))
    else: sels=[1]
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


def lucky(): #same concept as google's feeling lucky

    keys=input('Enter search keys: ').split(',')
    idList=[]
    obs={}

    for key in keys:
        try: obs.update(getObs(searchTitle(key),key))
        except: print('Search error: ', key)

    return obs

def writeMeta(l, fname): #collects and writes meta data; same for all module

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

def printCSV(obs): #prints csv

    print('Would you like to record for all dates (A) or all compatible dates (C)?')
    if input().upper()=='C': op=operator.and_
    else: op=operator.or_

    fileName=input("Enter file name to write to: ")
    with open(fileName, "w") as file:
        wr=csv.writer(file)

        keys=["dates"]
        for k in obs.keys(): keys.append(k)
        wr.writerow(keys) #successfully writes row of dates and id's

        dates=collectDates(obs, op)
        if dates==[] and op==operator.and_:
                print("No compatible dates; recording all dates.")
                dates=collectDates(obs, operator.or_)

        for d in dates:
            l=[d]
            for k in range(1,len(keys)):
                if d not in obs[keys[k]].keys():
                    l.append('.')
                else:
                    l.append(obs[keys[k]][d])
            wr.writerow(l)

        if input('Would you like to record meta data?(Y/N): ').upper()=='Y':
            writeMeta(list(obs.keys()), fileName)#defaults to no


def FRBapi(): #main loop

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
