from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query
import os
import glob
from datetime import datetime

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

def format_date(date_str):
    # Convert from format YYYY-MM-DD-HH-MM-SS to YYYY/MM/DD HH:MM:SS
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d-%H-%M-%S')
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    except:
        return date_str

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
        submission['formatted_date'] = format_date(submission['date'])
        # Make URL absolute by adding Kaggle base URL if it's not already absolute
        if submission['url'] and not submission['url'].startswith('http'):
            submission['url'] = f"https://www.kaggle.com{submission['url']}"
    
    # Create competition submissions page URL
    submissions_page_url = f"https://www.kaggle.com/competitions/{competition_name}/submissions"
    
    return render_template('competition.html', 
                         competition_name=competition_name,
                         submissions=submissions,
                         submissions_page_url=submissions_page_url)

@app.route('/save_notes', methods=['POST'])
def save_notes():
    data = request.get_json()
    competition_name = data.get('competition_name')
    submission_url = data.get('submission_url')
    notes = data.get('notes')

    if not all([competition_name, submission_url]):
        return jsonify({'success': False, 'error': 'Missing required fields'})

    try:
        db = TinyDB(f'db/{competition_name}.json')
        Submission = Query()
        db.update({'notes': notes}, Submission.url == submission_url)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 