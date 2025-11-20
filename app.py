from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import fcntl
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# Configuration
DATA_FILE = os.getenv('DATA_FILE', 'data/nhs_submissions.json')
PORT = int(os.getenv('PORT', 5000))

# Form Choice Constants
# These values correspond to the option values in the form templates
GENDER_CHOICES = {
    'MALE': '1',
    'FEMALE': '2',
    'NON_BINARY': '3'
}

ETHNICITY_CHOICES = {
    'WHITE_BRITISH': '1',
    'MIXED': '2',
    'ASIAN': '3',
    'BLACK': '4',
    'OTHER': '5',
    'WHITE_OTHER': '6',
    'WHITE_IRISH': '7'
}

EDUCATION_LEVELS = {
    'NO_QUALIFICATIONS': '1',
    'LEVEL_1': '2',  # Up to 4 GCSEs
    'LEVEL_2': '3',  # 5+ GCSEs or 1 A level
    'LEVEL_3': '4',  # 2+ A levels
    'LEVEL_4_PLUS': '5',  # Degree or professional qualification
    'APPRENTICESHIP': '6'
}

DISABILITY_STATUS = {
    'LIMITED_A_LOT': '1',
    'LIMITED_A_LITTLE': '2',
    'NO': '3'
}

NHS_SATISFACTION = {
    'VERY_SATISFIED': '1',
    'QUITE_SATISFIED': '2',
    'NEITHER': '3',
    'QUITE_DISSATISFIED': '4',
    'VERY_DISSATISFIED': '5'
}


def load_submissions():
    """Load existing submissions from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_submission(data):
    """
    Save a new submission to the JSON file with file locking.
    Uses fcntl for Unix/Linux/Mac systems to prevent race conditions.
    """
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # Open file in read-write mode, create if doesn't exist
    with open(DATA_FILE, 'a+') as f:
        # Acquire exclusive lock
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)

        try:
            # Move to beginning and read existing data
            f.seek(0)
            content = f.read()

            if content:
                submissions = json.loads(content)
            else:
                submissions = []

            # Generate ID and timestamp
            data['id'] = len(submissions) + 1
            data['timestamp'] = datetime.now().isoformat()

            submissions.append(data)

            # Write updated data
            f.seek(0)
            f.truncate()
            json.dump(submissions, f, indent=2)

            return data['id']
        finally:
            # Release lock
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def validate_eligibility(form_data):
    """Validate Step 1: Eligibility fields."""
    errors = []
    if not form_data['canAttend']:
        errors.append('You must confirm you can attend all dates.')
    if not form_data['isEligible']:
        errors.append('You must confirm you are eligible to attend.')
    return errors


def validate_contact_details(form_data):
    """Validate Step 2: Contact Details."""
    errors = []
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
    return errors


def validate_about_you(form_data):
    """Validate Step 3: About You fields."""
    errors = []
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
    return errors


def validate_consent(form_data):
    """Validate Step 4: Consent."""
    errors = []
    if not form_data['dataConsent']:
        errors.append('You must consent to the use of your data.')
    return errors


def validate_form(form_data):
    """Main validation orchestrator."""
    errors = []
    errors.extend(validate_eligibility(form_data))
    errors.extend(validate_contact_details(form_data))
    errors.extend(validate_about_you(form_data))
    errors.extend(validate_consent(form_data))
    return errors


@app.route('/')
def index():
    """Display the NHS conversation registration form."""
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with validation."""
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

    # Validate form data
    errors = validate_form(form_data)

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
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=PORT)
