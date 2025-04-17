from flask import Flask, render_template
from tinydb import TinyDB
import os
import glob

app = Flask(__name__)

@app.route('/')
def index():
    # Get list of all database files
    db_files = glob.glob('db/*.json')
    competitions = [os.path.splitext(os.path.basename(f))[0] for f in db_files]
    return render_template('index.html', competitions=competitions)

@app.route('/competition/<competition_name>')
def competition(competition_name):
    db = TinyDB(f'db/{competition_name}.json')
    submissions = db.all()
    # Sort submissions by date in descending order
    submissions.sort(key=lambda x: x['date'], reverse=True)
    return render_template('competition.html', 
                         competition_name=competition_name,
                         submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True) 