import time
from tinydb import TinyDB, Query
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
    # TODO: maybe add all sumissions that aren't in the database in the future?

    db = TinyDB('db.json')

    while 1:
        subs = api.competition_submissions('czii-cryo-et-object-identification')

        for sub in subs:
            if sub.status == 'pending' and not db.search(Query().url == sub.url):
                print(f'adding new entry {sub.url}')
                db.insert(
                    {'url': sub.url, 'status': sub.status, 'date': fmt_dt(sub.date), 'description': sub.description})

        for sub in api.competition_submissions('czii-cryo-et-object-identification'):
            # 上の処理でpendingとしてdbに記録されてる奴のみ処理する
            if not db.search(Query().url == sub.url):
                continue

            # sub.dateが申請した時間で固定されてる前提の実装
            # 終了後、終了時間に変わるなら練り直しが必要
            elapsed = datetime.utcnow() - sub.date
            print(f'{sub.date} [elapsed={elapsed}] "{sub.description}" ')
            if sub.status != 'pending':
                print(f'submission => {sub.status} sub.date={sub.date} elapsed={elapsed}')
                db.update({'status': sub.status, 'duration': elapsed.seconds}, Query().url == sub.url)
                break

        time.sleep(60)
