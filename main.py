from tinydb import TinyDB, Query
import time
import pickle
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


def get_pending_subs(api):
    submissions = api.competition_submissions('czii-cryo-et-object-identification')
    return list(filter(lambda x: x.status == 'pending', submissions))


if __name__ == '__main__':
    api = KaggleApi()
    api.authenticate()
    pending = get_pending_subs(api)

    # TODO: maybe add all sumissions that aren't in the database in the future?

    db = TinyDB('db.json')

    # TODO: まとめて出来ない？
    for sub in pending:
        if not db.search(Query().url == sub.url):
            print(f'adding new entry {sub.url}')
            db.insert({'url': sub.url, 'status': sub.status, 'date': fmt_dt(sub.date), 'description': sub.description})

    urls = [p.url for p in pending]

    while 1:
        subs = [sub for sub in api.competition_submissions('czii-cryo-et-object-identification') if sub.url in urls]
        if not subs:
            break
        for sub in subs:
            # sub.dateが申請した時間で固定されてる前提の実装
            # 終了後、終了時間に変わるなら練り直しが必要
            elapsed = datetime.utcnow() - sub.date
            print(f'{sub.date}[elapsed={elapsed}]')
            if sub.status != 'pending':
                print(f'submission => {sub.status} sub.date={sub.date} elapsed={elapsed}')
                db.update({'status': sub.status, 'duration': elapsed.seconds}, Query().url == sub.url)
                break
        time.sleep(60)

    with open('elapsed.pickle', 'wb') as f:
        pickle.dump(elapsed, f)
