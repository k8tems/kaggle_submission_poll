from flask import Flask, render_template
from tinydb import TinyDB
import os
import glob

app = Flask(__name__)

def format_duration(seconds):
    if seconds is None:
        return '-'
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    elif minutes > 0:
        return f"00:{minutes:02d}:{remaining_seconds:02d}"
    else:
        return f"00:00:{remaining_seconds:02d}"

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
    submissions.sort(key=lambda x: x['date'], reverse=True)
    
    for submission in submissions:
        submission['formatted_duration'] = format_duration(submission.get('duration'))
        # Make URL absolute by adding Kaggle base URL if it's not already absolute
        if submission['url'] and not submission['url'].startswith('http'):
            submission['url'] = f"https://www.kaggle.com{submission['url']}"
    
    return render_template('competition.html', 
                         competition_name=competition_name,
                         submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True) 