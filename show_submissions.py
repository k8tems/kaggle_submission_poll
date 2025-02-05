from tinydb import TinyDB, Query


if __name__ == '__main__':
    db = TinyDB('db.json')

    for row in db.search(Query().duration != None):
        print(row['date'], f'{row["duration"] / 3600:.02f} hrs', row['description'])
