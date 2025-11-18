# Job Assessment Form - Project Information

## Project Overview

This is a Flask-based web application designed for job assessment forms. It uses a simple text file (JSON) as a database, making it lightweight and easy to deploy without external database dependencies.

## Technology Stack

- **Backend**: Python 3.x with Flask 3.0.0
- **Frontend**: HTML5, CSS3 (no JavaScript framework)
- **Storage**: JSON file-based storage
- **Template Engine**: Jinja2 (built into Flask)

## Project Structure

```
gazda-assesment-form/
├── .claude/
│   ├── project-info.md          # This file - project documentation
│   └── prompts/                 # Conversation history with Claude
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── README.md                   # Setup and usage instructions
├── .gitignore                  # Git ignore rules
├── data/
│   └── submissions.json        # JSON file storing form submissions (auto-created)
├── templates/
│   ├── form.html              # Main assessment form template
│   └── success.html           # Success confirmation page
└── static/
    └── css/
        └── style.css          # Application styles
```

## Core Files Description

### app.py (Main Application)
- Flask application with routes for form display and submission
- Form validation logic
- JSON file read/write operations
- Flash message handling for errors
- Default port: 5000

**Key Functions:**
- `load_submissions()` - Loads all submissions from JSON file
- `save_submission(data)` - Saves new submission with ID and timestamp
- Routes: `/` (form), `/submit` (POST handler), `/success` (confirmation)

### templates/form.html
- Main job assessment form
- Fields: name, email, phone, position, experience, skills
- Client-side HTML5 validation attributes
- Flash message display for server-side errors
- Responsive design

### templates/success.html
- Success confirmation page after form submission
- Option to submit another application
- Clean, centered design with success icon

### static/css/style.css
- Modern gradient UI (purple/blue theme)
- Responsive design for mobile and desktop
- Form styling with focus states
- Button hover effects
- Alert/message styling

### data/submissions.json
- Auto-created on first submission
- Each submission includes:
  - `id`: Auto-incrementing number
  - `timestamp`: ISO format timestamp
  - All form fields (name, email, phone, position, experience, skills)

## Configuration

### Secret Key
Location: `app.py`
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```
**Important**: Change this in production environments!

### Port Configuration
Location: `app.py` (last line)
```python
app.run(debug=True, port=5000)
```

### Debug Mode
Currently set to `True` for development. Set to `False` for production.

## Form Fields

### Required Fields
- Full Name (min 2 characters)
- Email Address (must contain @)
- Position Applied For (dropdown)
- Years of Experience (dropdown)

### Optional Fields
- Phone Number
- Key Skills & Technologies (textarea)

### Position Options
- Frontend Developer
- Backend Developer
- Full Stack Developer
- DevOps Engineer
- QA Engineer
- Project Manager
- Other

### Experience Ranges
- 0-1 years
- 1-3 years
- 3-5 years
- 5-10 years
- 10+ years

## Validation Rules

Server-side validation in `app.py` checks:
1. Name: Required, min 2 characters
2. Email: Required, must contain @
3. Position: Required
4. Experience: Required

Validation errors are displayed via Flask flash messages.

## Data Flow

1. User fills out form at `/`
2. Form submits POST to `/submit`
3. Server validates input
4. If invalid: redirect to `/` with error messages
5. If valid: save to JSON file and redirect to `/success`

## Development Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## Common Tasks

### View Submissions
```bash
cat data/submissions.json
# or formatted:
python -m json.tool data/submissions.json
```

### Change Port
Edit `app.py` line 63 (or last line)

### Add Form Fields
1. Add HTML input in `templates/form.html`
2. Update `submit()` function in `app.py` to capture field
3. Add validation if needed
4. Update `submission_data` dict to include new field

### Customize Styling
Edit `static/css/style.css`

## Security Considerations

- Change `app.secret_key` in production
- Set `debug=False` in production
- Add CSRF protection for production use
- Validate and sanitize all user inputs
- Consider adding rate limiting for production

## Future Enhancements (Ideas)

- Admin panel to view submissions
- Export submissions to CSV
- Email notifications on submission
- File upload capability
- Database migration (SQLite, PostgreSQL)
- User authentication
- CSRF token implementation
- API endpoints for submissions

## Dependencies

- Flask==3.0.0 - Web framework
- Werkzeug==3.0.1 - WSGI utility library (Flask dependency)

## Notes

- This is a minimal implementation for assessment purposes
- No external database required
- All data persists in `data/submissions.json`
- Virtual environment recommended for isolation
- Compatible with Python 3.7+
