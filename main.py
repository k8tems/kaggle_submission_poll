import time
import pickle
import pytz
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta


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

    while 1:
        subs = api.competition_submissions('czii-cryo-et-object-identification')
        sub = subs[0]
        elapsed = datetime.now(tz=pytz.timezone('Asia/Tokyo')) - init_date.replace(
            tzinfo=pytz.timezone('Asia/Tokyo')) - timedelta(hours=9)
        print(f'{sub.date}[{elapsed}]')
        if sub.status == 'complete':
            print(f'submission complete! sub.date={sub.date}')
            break
        time.sleep(10)

    with open('elapsed.pickle', 'wb') as f:
        pickle.dump(elapsed, f)
