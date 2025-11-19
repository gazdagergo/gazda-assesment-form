from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'nhs-conversation-secret-key-change-in-production'

# Data file path
DATA_FILE = 'data/nhs_submissions.json'


def load_submissions():
    """Load existing submissions from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_submission(data):
    """Save a new submission to the JSON file."""
    submissions = load_submissions()

    # Generate ID and timestamp
    data['id'] = len(submissions) + 1
    data['timestamp'] = datetime.now().isoformat()

    submissions.append(data)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

    return data['id']


@app.route('/')
def index():
    """Display the NHS conversation registration form."""
    return render_template('form_nhs.html')


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with validation."""
    errors = []

    # Get form data
    form_data = {
        # Eligibility
        'canAttend': request.form.get('canAttend') == 'on',
        'isEligible': request.form.get('isEligible') == 'on',
        # Contact Details
        'firstName': request.form.get('firstName', '').strip(),
        'lastName': request.form.get('lastName', '').strip(),
        'email': request.form.get('email', '').strip(),
        'phone': request.form.get('phone', '').strip(),
        'address1': request.form.get('address1', '').strip(),
        'address2': request.form.get('address2', '').strip(),
        'city': request.form.get('city', '').strip(),
        'postCode': request.form.get('postCode', '').strip(),
        # About You
        'gender': request.form.get('gender', ''),
        'dobDay': request.form.get('dobDay', ''),
        'dobMonth': request.form.get('dobMonth', ''),
        'dobYear': request.form.get('dobYear', '').strip(),
        'ethnicity': request.form.get('ethnicity', ''),
        'disability': request.form.get('disability', ''),
        'nhsSatisfaction': request.form.get('nhsSatisfaction', ''),
        'education': request.form.get('education', ''),
        # Consent
        'dataConsent': request.form.get('dataConsent') == 'on',
        'futureContact': request.form.get('futureContact') == 'on',
    }

    # Validation
    # Step 1: Eligibility
    if not form_data['canAttend']:
        errors.append('You must confirm you can attend all dates.')
    if not form_data['isEligible']:
        errors.append('You must confirm you are eligible to attend.')

    # Step 2: Contact Details
    if not form_data['firstName']:
        errors.append('First name is required.')
    if not form_data['lastName']:
        errors.append('Last name is required.')
    if not form_data['email'] or '@' not in form_data['email']:
        errors.append('A valid email address is required.')
    if not form_data['phone']:
        errors.append('Phone number is required.')
    if not form_data['address1']:
        errors.append('Address line 1 is required.')
    if not form_data['city']:
        errors.append('City is required.')
    if not form_data['postCode']:
        errors.append('Post code is required.')

    # Step 3: About You
    if not form_data['gender']:
        errors.append('Gender is required.')
    if not form_data['dobDay']:
        errors.append('Day of birth is required.')
    if not form_data['dobMonth']:
        errors.append('Month of birth is required.')
    if not form_data['dobYear']:
        errors.append('Year of birth is required.')
    elif not form_data['dobYear'].isdigit() or len(form_data['dobYear']) != 4:
        errors.append('Please enter a valid 4-digit year.')
    if not form_data['ethnicity']:
        errors.append('Ethnic group is required.')
    if not form_data['disability']:
        errors.append('Disability status is required.')
    if not form_data['nhsSatisfaction']:
        errors.append('NHS satisfaction response is required.')
    if not form_data['education']:
        errors.append('Educational qualification is required.')

    # Step 4: Consent
    if not form_data['dataConsent']:
        errors.append('You must consent to the use of your data.')

    # If validation errors, flash them and redirect back
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('index'))

    # Save submission
    submission_id = save_submission(form_data)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    """Display success confirmation page."""
    return render_template('success_nhs.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
