##control module
##How to specify which api to use in search -> each module has own search method,
##that method is called by method that has API as arg
##How to handle the python 2.7 code?
        ## see -> https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3

#This project takes advantage of existing APIs found at
#https://research.stlouisfed.org/docs/api/fred/

from urllib.request import urlopen
import operator
import datetime
import json
import csv

import FRBapi
import fred_API
#import python27api
import scratchAPI


def writeMeta(l, fname): #collects and writes meta data

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
            file.write(data['seriess'][0]['seasonal_adjustment']+ '\n'+ 'frequency: ' +
                        data['seriess'][0]['frequency']+' units: '+ data['seriess'][0]['units']+'\n')
            file.write('start: '+ data['seriess'][0]['observation_start']+ ' end:'+
                       data['seriess'][0]['observation_end']+'\n \n ---------------- \n ---------------- \n')
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



def mainLoop(): #main loop

    obs, more={}, True
    #if input('Feeling lucky? (Y/N): ').upper()=='Y':
     #   obs, more=lucky(), False #TODO


    APIs = {'1' : FRBapi.searchTitle, '2' : fred_API.searchTitle,
             '3' : scratchAPI.searchTitle} #TODO add way to call python 27 api


    api_choice = None

    while(api_choice not in APIs.keys()):
        print("Select API")
        print(" 1) FRB\n 2) FRED\n 3) scratch")
        api_choice = input()

    #feelingLucky = (input('Feeling lucky? (Y/N): ').upper()=='Y')

    while(more):
        obs.update(APIs[api_choice]()) #TODO
        if input("Search Again(Y/N): ").upper() == 'N': #defaults to yes
            break

    if obs!={}: printCSV(obs) #TODO
    else: print('no data recorded -> good bye :)')

if __name__=="__main__":
    mainLoop()
