#fred api data collection

#This project uses fredapi provided at
#https://github.com/mortada/fredapi

from fredapi import Fred

fred=Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e')

def searchTitle(searchKey , lucky=False): #searches for items matching search key
                        #returns list of responses

        #if not args: searchKey=input("Enter search key: ")
        #else: searchKey=args[0]
        df=fred.search(searchKey).T
        titles=df.columns.values.tolist()
        l=[]
        index=1
        for t in titles:
                temp=df[t].values.tolist()
                l.append((temp[12],t)) #TODO review and document what this is
                index+=1
                if index==51: break

        return l #returns list of tuples (series title, series id)


def getObs(series_ID):
    #Need to return dict {series{}}
    obs={} #dict{'seriesID': {'date':value}}

    try:
        res=fred.get_series_latest_release(series_ID)
        obs[series_ID]=dict(zip(res.keys(),res.values)) #TODO does not have date
    except:
        print('Invalid data selection: ', series_ID)

    return obs #return dict{series ID, {date, value}}
