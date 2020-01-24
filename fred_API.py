# fred api data collection

# This project uses fredapi provided at
# https://github.com/mortada/fredapi #TODO doc string this

from fredapi import Fred

fred = Fred(api_key='3b7e7d31bcc6d28556c82c290eb3572e')

def search_title(search_key, lucky = False):
    """
    searches for items matching searchKey
     returning a list of returning list of tuple(datetimet, series id)
    :param search_key:
    :param lucky:
    :return:
    """

    df = fred.search(search_key).T
    titles = df.columns.values.tolist()
    ret_list = []
    index = 1
    for t in titles:
        temp = df[t].values.tolist()
        ret_list.append((temp[3], t))  # TODO review and document what this is
        index += 1
        if index == 51 or lucky :
            break
    return ret_list


def get_obs(series_ID):
    """
    collect observations for a given series_ID
    :param series_ID: the fred series id key to search for
    :return: dict{series ID, {date, value}}
    """
    obs = {}
    try:
        res = fred.get_series_latest_release(series_ID)
        obs[series_ID] = dict(zip(res.keys(), res.values))
    except:
        print('Invalid data selection: ', series_ID)

    return obs
# TODO failing lucky with search for GDP....
