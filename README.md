# NHS Conversation Registration Form - Flask Application

A Flask-based web application for NHS conversation event registration with JSON file storage.

## Features

- Multi-step registration form with progress tracking
- Comprehensive form validation
- JSON-based file storage (no database required)
- Success confirmation page
- Modern, responsive UI with NHS-inspired styling
- Flash messages for validation errors

## Project Structure

```
gazda-assesment-form/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── data/
│   └── nhs_submissions.json # JSON file storing form submissions (created on first submission)
├── templates/
│   ├── form.html          # NHS registration form template
│   └── success.html       # Success confirmation page
└── static/
    └── css/
        └── style.css      # Application styles
```

## Installation

1. Navigate to the project directory:
```bash
cd /Users/macbookair/Sites/gazda-assesment-form
```

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Create a `.env` file for configuration:
```bash
cp .env.example .env
```

Then edit `.env` to customize your settings (secret key, port, etc.).

## Running the Application

1. Make sure your virtual environment is activated

2. Run the Flask app:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Submitting a Registration

The registration form consists of four steps:

1. **Eligibility**
   - Confirm ability to attend all event dates
   - Confirm eligibility to attend

2. **Contact Details**
   - First Name (required)
   - Last Name (required)
   - Email Address (required)
   - Phone Number (required)
   - Address Line 1 (required)
   - Address Line 2 (optional)
   - City (required)
   - Post Code (required)

3. **About You**
   - Gender (required)
   - Date of Birth (required)
   - Ethnic Group (required)
   - Disability Status (required)
   - NHS Satisfaction (required)
   - Educational Qualification (required)

4. **Consent & Submit**
   - Data Usage Consent (required)
   - Future Contact Opt-in (optional)

Click "Submit Registration" to complete. If validation passes, you'll be redirected to a success page. Form data is saved to `data/nhs_submissions.json`.

### Viewing Submissions

Submissions are stored in `data/nhs_submissions.json`. You can view them by opening the file:

```bash
cat data/nhs_submissions.json
```

Or in a more readable format:
```bash
python -m json.tool data/nhs_submissions.json
```

## Data Format

Each submission is stored as a JSON object with the following structure:

```json
{
  "id": 1,
  "timestamp": "2025-11-20T10:30:00.123456",
  "canAttend": true,
  "isEligible": true,
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+44 20 1234 5678",
  "address1": "123 Main Street",
  "address2": "Flat 4",
  "city": "London",
  "postCode": "SW1A 1AA",
  "gender": "male",
  "dobDay": "15",
  "dobMonth": "06",
  "dobYear": "1990",
  "ethnicity": "white-british",
  "disability": "no",
  "nhsSatisfaction": "satisfied",
  "education": "degree",
  "dataConsent": true,
  "futureContact": true
}
```

## Configuration

The application can be configured using environment variables. Create a `.env` file in the project root (see `.env.example` for reference):

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True

# Application Configuration
PORT=5000
DATA_FILE=data/nhs_submissions.json
```

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management (required for production)
- `DEBUG`: Enable/disable debug mode (True/False)
- `PORT`: Port number for the application (default: 5000)
- `DATA_FILE`: Path to the JSON file for storing submissions

### Generating a Secure Secret Key

For production, generate a secure secret key:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Add this to your `.env` file as `SECRET_KEY=<generated-key>`

### Customizing Form Fields

Edit `templates/form.html` to add or modify form fields. Update the validation logic in `app.py` in the `submit()` function accordingly.

## Development

The application runs in debug mode by default (`debug=True`), which provides:
- Auto-reload on code changes
- Detailed error pages
- Interactive debugger

For production deployment, set `debug=False`.

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, change the port number in `app.py` or kill the process using that port:

```bash
lsof -ti:5000 | xargs kill -9
```

### Virtual Environment Issues

If you encounter issues with the virtual environment:

```bash
deactivate  # Exit current venv
rm -rf venv  # Remove old venv
python3 -m venv venv  # Create new venv
source venv/bin/activate  # Activate
pip install -r requirements.txt  # Reinstall dependencies
```

## License

This is a simple assessment project and is provided as-is for educational purposes.
