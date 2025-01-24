import time
from tinydb import TinyDB, Query
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    api = KaggleApi()
    api.authenticate()

    db = TinyDB('db.json')

    while 1:
        subs = api.competition_submissions('czii-cryo-et-object-identification')

        for sub in subs:
            if not db.search(Query().url == sub.url):
                print(f'adding new entry {sub.description}')
                db.insert(
                    {'url': sub.url, 'status': sub.status, 'date': fmt_dt(sub.date), 'description': sub.description})

        for sub in api.competition_submissions('czii-cryo-et-object-identification'):
            if not db.search((Query().url == sub.url) & (Query().status == 'pending')):
                continue

            # sub.dateが申請した時間で固定されてる前提の実装
            # 終了後、終了時間に変わるなら練り直しが必要
            elapsed = datetime.utcnow() - sub.date
            print(f'{sub.date} [elapsed={elapsed}] "{sub.description}" ')
            if sub.status != 'pending':
                print(f'submission => {sub.status} sub.date={sub.date} elapsed={elapsed}')
                db.update({'status': sub.status, 'duration': elapsed.seconds}, Query().url == sub.url)

        time.sleep(60)
