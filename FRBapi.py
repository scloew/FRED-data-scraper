#FRB api for net centric final project

#does compatible dates work :: nan values recorded - should I check for nan's?

#This project uses FRB api provided at
#https://github.com/avelkoski/FRB

from fred import Fred

fr = Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e', response_type='dict')

def searchTitle(searchKey, lucky=False): #finds series titles #TODO refactor this; not single purpose (i.e use helpers)
                                                              #TODO better naming skills
    params={'limit':50}
    print(searchKey)
    searchRes=fr.series.search(searchKey, params=params)
    series = []
    print('check 1')
    for result in searchRes:
        series.append((result['title'], result['id']))
        if lucky: break

    return series #list of tuples (seried title, fRED id)

def getObs(series_ID):

    obs = {}

    params = {
         'limit':10000,
         'output_type':1
         }
    tempD = dict({series_ID : fr.series.observations(series_ID, params=params)})
    for d in tempD[series_ID]:
        obs[d['date']]=d['value']

    return {series_ID : obs}
    #return dict{series ID, {date, value}}
