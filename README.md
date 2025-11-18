# Job Assessment Form - Flask Application

A simple Flask-based web application for job assessment forms with JSON file storage.

## Features

- Clean, responsive form interface
- Server-side form validation
- JSON-based file storage (no database required)
- Success confirmation page
- Modern gradient UI with basic styling
- Flash messages for validation errors

## Project Structure

```
gazda-assesment-form/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── data/
│   └── submissions.json    # JSON file storing form submissions (created on first submission)
├── templates/
│   ├── form.html          # Main form template
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

### Submitting a Form

1. Fill out the form fields:
   - Full Name (required)
   - Email Address (required)
   - Phone Number (optional)
   - Position Applied For (required)
   - Years of Experience (required)
   - Key Skills & Technologies (optional)

2. Click "Submit Application"

3. If validation passes, you'll be redirected to a success page

4. Form data is saved to `data/submissions.json`

### Viewing Submissions

Submissions are stored in `data/submissions.json`. You can view them by opening the file:

```bash
cat data/submissions.json
```

Or in a more readable format:
```bash
python -m json.tool data/submissions.json
```

## Data Format

Each submission is stored as a JSON object with the following structure:

```json
{
  "id": 1,
  "timestamp": "2025-11-18T10:30:00.123456",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+36 XX XXX XXXX",
  "position": "fullstack-developer",
  "experience": "3-5",
  "skills": "Python, Flask, JavaScript, React"
}
```

## Configuration

### Changing the Secret Key

In production, change the secret key in `app.py`:

```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

Generate a secure secret key:
```bash
python -c 'import secrets; print(secrets.token_hex(16))'
```

### Changing the Port

To run on a different port, modify the last line in `app.py`:

```python
app.run(debug=True, port=5000)  # Change port number here
```

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