import time
from tinydb import TinyDB, Query
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime
from pprint import pprint


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    db = TinyDB('db.json')

    for row in db.search(Query().duration != None):
        print(row['date'], f'{row["duration"] / 3600:.02f} hrs', row['description'])
