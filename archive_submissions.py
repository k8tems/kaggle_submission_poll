import sys
from tinydb import TinyDB, Query
from kaggle.api.kaggle_api_extended import KaggleApi


def fmt_dt(dt):
    return dt.strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python archive_submissions.py <competition_name>")
        sys.exit(1)

    competition_name = sys.argv[1]
    api = KaggleApi()
    api.authenticate()

    # Open the database
    db = TinyDB(f'db/{competition_name}.json')
    subs = api.competition_submissions(competition_name)
    new_entries = 0

    for sub in subs:
        if sub.status.name != 'COMPLETE':
            continue

        if db.search(Query().url == sub.url):
            continue

        print(f'Adding submission: {sub.description} (Score: {sub.public_score})')
        db.insert({
            'url': sub.url,
            'status': sub.status.name,
            'date': fmt_dt(sub.date),
            'description': sub.description,
            'public_score': sub.public_score
        })
        new_entries += 1

    print(f"\nComplete:")
    print(f"- Found {len(subs)} total submissions")
    print(f"- Added {new_entries} new completed submissions")
    print(f"- Total submissions in database: {len(db.all())}") 
