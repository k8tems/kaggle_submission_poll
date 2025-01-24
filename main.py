from tinydb import TinyDB, Query
import time
import pickle
import pytz
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


def get_pending_subs(api):
    submissions = api.competition_submissions('czii-cryo-et-object-identification')
    return list(filter(lambda x: x.status == 'pending', submissions))


if __name__ == '__main__':
    api = KaggleApi()
    api.authenticate()
    pending = get_pending_subs(api)

    # とりあえず一個
    sub = pending[0]
    init_date = sub.date

    db = TinyDB('db.json')
    if not db.search(Query().url == sub.url):
        print(f'adding new entry {sub.url}')
        db.insert({'url': sub.url, 'status': sub.status, 'date': fmt_dt(sub.date), 'description': sub.description})

    while 1:
        subs = api.competition_submissions('czii-cryo-et-object-identification')
        sub = subs[0]
        elapsed = datetime.utcnow() - init_date
        print(f'{sub.date}[elapsed={elapsed}]')
        if sub.status != 'pending':
            print(f'submission => {sub.status} sub.date={sub.date} elapsed={elapsed}')
            db.update({'status': sub.status, 'duration': elapsed.seconds}, Query().url == sub.url)
            break
        time.sleep(60)

    with open('elapsed.pickle', 'wb') as f:
        pickle.dump(elapsed, f)
