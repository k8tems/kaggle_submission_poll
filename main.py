import sys
import time
from tinydb import TinyDB, Query
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    api = KaggleApi()
    api.authenticate()
    competition_name = sys.argv[1]

    db = TinyDB(competition_name)

    while 1:
        subs = api.competition_submissions(competition_name)

        for sub in subs:
            if not db.search(Query().url == sub.url):
                print(f'adding new entry {sub.description}')
                db.insert(
                    {'url': sub.url, 'status': sub.status.name, 'date': fmt_dt(sub.date), 'description': sub.description})

            if not db.search((Query().url == sub.url) & (Query().status == 'PENDING')):
                continue

            # sub.dateが申請した時間で固定されてる前提の実装
            # 終了後、終了時間に変わるなら練り直しが必要
            elapsed = datetime.utcnow() - sub.date
            print(f'{sub.date} [elapsed={elapsed}] "{sub.description}" ')
            if sub.status != 'pending':
                print(f'submission => {sub.status.name} publicScore={sub.public_score} sub.date={sub.date} elapsed={elapsed}')
                db.update({'status': sub.status.name, 'duration': elapsed.seconds}, Query().url == sub.url)

        time.sleep(60)
