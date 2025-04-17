import sys
from tinydb import TinyDB, Query


if __name__ == '__main__':
    competition_name = sys.argv[1]
    db = TinyDB(f'db/{competition_name}.json')

    for row in db.search(Query().duration != None):
        print(row['date'], f'{row["duration"] / 3600:.02f} hrs', row['description'])
