#Net centric third api
#compatibility issues w/ python 3 -> written to run on python 2.7

#This project uses FRB api provided at
#https://github.com/zachwill/fred

import fred
import urllib2
import sys
import csv
import datetime
import json
import operator

def searchTitle(*args):

    if not args: searchKey=raw_input("Enter search key: ")
    else: searchKey=args[0]
    response=fred.search(searchKey)
    if response['seriess']==[]:
        print 'No results found for: ', searchKey
        return []
    index=1
    l=['']
    i=0
    if not args: print '0) ALL'
    while i <len(response['seriess']) and index<51:
        if not args: sys.stdout.write(str(index)), sys.stdout.write(') ')
        more=True #necessary?
        if i <len(response['seriess']):
            try:
                l.append((response['seriess'][i]['title'],response['seriess'][i]['id']))
                if args: break
                print response['seriess'][i]['title']
                i+=1
                index+=1
            except:
                i+=1
        if args: break

    return l


def	getObs(l, *args): #takes list from searchTitle and gets obs

    if l==[]: return {}
    if not args:
        sels=raw_input('Enter selection: ')
        sels=sels.split(' ')
        if '0' in sels: sels=range(1,len(l))
    else: sels=[1]

    obs={} #dict{'seriesID': {'date':value}}
    for i in sels:
        try:
            res=fred.observations(l[(int(i))][1])
            tempD={}
            for item in res['observations']:
                tempD[item['date']]=item['value']
            obs[l[(int(i))][1]]=tempD
        except:
            print 'Invalid data selection: ', i

    return obs

def writeMeta(l, fname): #throwing error for some reason

    mname=fname[:fname.rfind('.')]+'Meta.txt'
    print 'writing to: ', mname

    with open(mname, 'w') as file:
        file.write('Accessed '+ str(datetime.date.today())+'\n \n \n')
        for ID in l:
            key='&api_key=3b7e7d31bcc6d28556c82c290eb3572e&file_type=json'
            url='https://api.stlouisfed.org/fred/series?series_id='+ID+key
            response=urllib2.urlopen(url)
            content=response.read()
            data=json.loads(content.decode('utf8'))
            file.write(ID+'\n')
            try:file.write(data['seriess'][0]['title']+'\n')
            except: file.write('Title error \n')
            file.write(data['seriess'][0]['seasonal_adjustment']+ '\n'+ 'frequency: ')
            file.write(data['seriess'][0]['frequency']+' units: '+ data['seriess'][0]['units']+'\n')
            file.write('start: '+data['seriess'][0]['observation_start']+' end: ' + data['seriess'][0]['observation_end'])
            file.write('\n \n ---------------- \n ---------------- \n')
        file.close()


def collectDates(obs, op):

    dates=set(obs[list(obs.keys())[0]].keys())
    for o in obs.keys():
        temp=set(obs[o].keys())
        dates=op(dates,temp)

    dates=sorted(dates)
    return dates


def printCSV(obs):

    print 'Would you like to record for all dates (A) or all compatible dates (C)?'
    if raw_input().upper()=='C': op=operator.and_
    else: op=operator.or_

    fileName=raw_input('Enter file name to write to: ')
    with open(fileName,"w") as file:
        wr=csv.writer(file)

        keys=['dates']
        for k in obs.keys(): keys.append(k)
        wr.writerow(keys)

        dates=collectDates(obs, op)
        if dates==[] and op==operator.and_:
            print 'No compatible dates; recording all dates'
            dates=collectDates(obs, operator.or_)

        for d in dates:
            l=[d]
            for k in range(1, len(keys)):
                if d not in obs[keys[k]].keys():
                    l.append('.')
                else:
                    l.append(obs[keys[k]][d])
            wr.writerow(l)
        file.close()

    if raw_input('Would you like to record meta data?(Y/N) ').upper()=='Y':
        writeMeta(list(obs.keys()), fileName)


def lucky():

    keys=raw_input('Enter search keys: ').split(', ')
    idList=[]
    obs={}

    for key in keys:
        try:obs.update(getObs(searchTitle(key), key))
        except: print('Search error', key)
    return obs
    
def thirdAPI(): #main loop

   fred.key('3b7e7d31bcc6d28556c82c290eb3572e')
   obs, more={}, True
   
   if raw_input('Feeling lucky? (Y/N): ').upper()=='Y':
        obs, more=lucky(), False
   
   while(more):
    obs.update(getObs(searchTitle()))
    if raw_input('Search again(Y/N) ').upper() == 'N':
        break

   if obs!= {}: printCSV(obs)
   else: print 'No data recorded -> good bye :)'

