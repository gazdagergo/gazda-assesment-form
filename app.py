from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

DATA_FILE = 'data/submissions.json'

def load_submissions():
    """Load submissions from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_submission(data):
    """Save a new submission to JSON file"""
    submissions = load_submissions()

    # Add timestamp and ID
    submission = {
        'id': len(submissions) + 1,
        'timestamp': datetime.now().isoformat(),
        **data
    }

    submissions.append(submission)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

@app.route('/')
def index():
    """Display the assessment form"""
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with validation"""
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    position = request.form.get('position', '').strip()
    experience = request.form.get('experience', '').strip()
    skills = request.form.get('skills', '').strip()

    # Validation
    errors = []
    if not name or len(name) < 2:
        errors.append('Name is required and must be at least 2 characters.')
    if not email or '@' not in email:
        errors.append('Valid email is required.')
    if not position:
        errors.append('Position is required.')
    if not experience:
        errors.append('Years of experience is required.')

    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('index'))

    # Save submission
    submission_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'position': position,
        'experience': experience,
        'skills': skills
    }

    save_submission(submission_data)

    return redirect(url_for('success'))

@app.route('/success')
def success():
    """Display success page"""
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)