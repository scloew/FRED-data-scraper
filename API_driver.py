##control module
##How to handle the python 2.7 code?
## see -> https://stackoverflow.com/questions/27863832/calling-python-2-script-from-python-3

# This project takes advantage of existing APIs found at
# https://research.stlouisfed.org/docs/api/fred/

from urllib.request import urlopen
import operator
import datetime
import json
import csv

import FRBapi
import fred_API
# import python27api
import scratchAPI


def record_meta(l, file_name):  # collects and writes meta data

    meta_name = file_name[:file_name.rfind('.')] + 'Meta.txt'
    print('writing to: ', meta_name)

    with open(meta_name, 'w') as meta_file:
        meta_file.write('Accessed ' + str(datetime.date.today()) + '\n' + '\n' + '\n')
        for ID in l:
            key = "&api_key=3b7e7d31bcc6d28556c82c290eb3572e&file_type=json"
            url = 'https://api.stlouisfed.org/fred/series?series_id=' + ID + key
            response = urlopen(url)
            content = response.read()
            data = json.loads(content.decode('utf8'))
            meta_file.write(ID + '\n')
            meta_file.write(data['seriess'][0]['title'] + '\n')
            meta_file.write(data['seriess'][0]['seasonal_adjustment'] + '\n' + 'frequency: ' +
                       data['seriess'][0]['frequency'] + ' units: ' + data['seriess'][0]['units'] + '\n')
            meta_file.write('start: ' + data['seriess'][0]['observation_start'] + ' end: ' +
                       data['seriess'][0]['observation_end'] +
                       '\n \n ---------------- \n ---------------- \n')  ##TODO use string interp; and better names
        meta_file.close()


def collect_dates(obs, op):
    dates = set((obs[(list(obs.keys()))[0]]).keys())
    for series in obs.keys():
        dates = op(dates, set(obs[series].keys()))
    return dates


def record_data(obs):  # prints csv

    print('Would you like to record for all dates (A) or all compatible dates (C)?')
    if input().upper() == 'C':
        op = operator.and_
    else:
        op = operator.or_

    dates = collect_dates(obs, op)

    if not dates and op == operator.and_:
        print("No compatible dates; recording all dates.")
        dates = collect_dates(obs, operator.or_)

    file_name = input("Enter file name to write to: ")
    with open(file_name, "w") as file:
        wr = csv.writer(file)

        header = ["dates"] + [k for k in obs.keys()]

        wr.writerow(header)

        for d in sorted(dates):
            data_row = [d]
            for series, observations in obs.items():
                if d in observations.keys():
                    data_row.append(observations[d])
                else:
                    data_row.append(None)
            wr.writerow(data_row)

        if input("Record meta data? (Y/N)").upper() == 'Y':
            record_meta(obs, file_name)


def print_search_results(search_res):
    index = 1
    for item in search_res:
        print(str(index) + ') ' + item[0])
        index += 1
        if index > 50:
            break


def main_loop():  # main loop

    obs, more = {}, True

    APIs = {'1': FRBapi, '2': fred_API,
            '3': scratchAPI}  # TODO add way to call python 27 api
    # TODO Each module will have get series method and get obs method

    api_choice = None

    while api_choice not in APIs.keys():
        print("Select API")
        print(" 1) FRB 2) FRED 3) scratch")
        api_choice = input()

    api = APIs[api_choice]
    lucky = (input('Feeling lucky? (Y/N): ').upper() == 'Y')

    while more:
        titles = input("Enter search keys comma delimited: ").split(',')
        for t in titles:
            search_res = api.searchTitle(t, lucky)
            if not lucky:
                print_search_results(search_res)
                selections = input("Enter Selections: ").split(' ')
            else:
                selections = [i for i in range(len(search_res))]

            for i in selections:
                obs.update(api.getObs(search_res[int(i)][1]))  # TODO need check for in bounds
        more = (input("Search Again(Y/N): ").upper() == 'Y')

    if obs:
        record_data(obs)
    else:
        print('no data recorded -> good bye :)')


if __name__ == "__main__":
    main_loop()
