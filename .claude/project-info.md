# Form Assessment System - Project Information

## Project Overview

This project demonstrates an **AI-aided form templating approach** using a declarative XML schema to define forms, which are then implemented as Flask/Alpine.js web applications. The initial POC is a job assessment form; the current work-in-progress is an NHS National Conversation application form.

## Technology Stack

- **Backend**: Python 3.x with Flask 3.0.0
- **Frontend**: HTML5, CSS3, Alpine.js 3.x with Persist plugin
- **Storage**: JSON file-based storage (server), localStorage (client drafts)
- **Template Engine**: Jinja2 (built into Flask)
- **Form Definition**: Custom XML DSL (form-template.xml)

## AI-Aided Templating Approach

The project uses a **declarative XML-based DSL** where:
1. `form-template.xml` defines the form structure, fields, validation, and behavior
2. The XML acts as a structured prompt for AI to generate working implementations
3. Implementation follows the patterns established in the POC

### XML Schema Elements

```xml
<!-- Root Element -->
<Form title="..." subtitle="..." action="/submit" method="POST" novalidate="true">

<!-- State Management (persistence) -->
<State persist="true" storageKey="draftKeyName">
  <Field name="fieldName" default="" />
</State>

<!-- Pagination -->
<Pagination totalSteps="N">
  <ProgressIndicator logic="..." />
</Pagination>

<!-- Form Sections -->
<FormSection step="1" title="Section Title">
  <!-- fields -->
</FormSection>

<!-- Field Types -->
<FormField name="..." label="..." type="text|email|tel" required="true" model="formData.field" />
<SelectField name="..." label="..." required="true" model="formData.field">
  <Option value="..." label="..." />
</SelectField>
<TextareaField name="..." label="..." rows="4" required="true" model="formData.field" />
<CheckboxField name="..." label="..." required="true" model="formData.field" />

<!-- Navigation -->
<Navigation>
  <PreviousButton label="..." />
  <NextButton label="..." />
  <SubmitButton label="..." />
  <ClearButton label="..." />
</Navigation>

<!-- Messages & Success -->
<Messages source="flask flash messages" />
<OnSuccess redirect="/success" />
```

### Common Field Attributes
- `name` - Form submission field name
- `label` - Display label
- `model` - Alpine.js x-model binding (e.g., `formData.fieldName`)
- `required` - Validation requirement
- `placeholder` - Input placeholder text
- `logic` - Documentation of the field's behavior

## Project Structure

```
gazda-assesment-form/
├── .claude/
│   ├── project-info.md              # This file - project documentation
│   └── prompts/
│       └── analysis-of-old-form/    # NHS form analysis
│           └── National conversation on the future of the NHS.html
├── app.py                           # Flask application
├── form-template.xml                # XML form definition (POC)
├── requirements.txt                 # Python dependencies
├── README.md                        # Setup instructions
├── data/
│   └── submissions.json             # Form submissions storage
├── templates/
│   ├── form.html                    # Main form (Alpine.js)
│   └── success.html                 # Success confirmation
└── static/
    └── css/
        └── style.css                # Application styles
```

## Implementation Patterns

### Alpine.js State Management

```javascript
x-data="{
  currentStep: 1,
  totalSteps: 2,
  formData: $persist({
    field1: '',
    field2: ''
  }).as('storageKey'),
  clearDraft() {
    this.formData = { field1: '', field2: '' };
    this.currentStep = 1;
  }
}"
```

### Multi-Step Pagination

- Controlled via `currentStep` state variable
- Sections use `x-show="currentStep === N"` with transitions
- Navigation buttons conditionally rendered based on step

### Progress Bar

- Visual indicator with percentage width: `(currentStep / totalSteps * 100)%`
- Step labels with dynamic bold styling for current step
- CSS transition for smooth animation

### Persistence

- **Client-side**: Alpine.js `$persist()` saves to localStorage automatically
- **Server-side**: Flask saves submissions to JSON file
- **On success**: localStorage cleared via `localStorage.removeItem('_x_storageKey')`

### Validation

- **Client-side**: HTML5 attributes (required, minlength, type)
- **Server-side**: Flask validation in `/submit` route
- **Errors**: Flask flash messages displayed in form

## Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display form |
| `/submit` | POST | Process submission |
| `/success` | GET | Show confirmation |

## Current POC: Job Assessment Form

### Fields
- Full Name (required, min 2 chars)
- Email Address (required)
- Phone Number (optional)
- Position Applied For (select, required)
- Years of Experience (select, required)
- Key Skills (textarea, optional)

### Steps
1. Personal Information (name, email, phone)
2. Professional Details (position, experience, skills)

---

## Work in Progress: NHS National Conversation Form

### Source Form Analysis

The original NHS form (`.claude/prompts/analysis-of-old-form/`) has these UX issues:
- Single long page - overwhelming
- Dense intro text with buried important info
- No progress indicator
- No draft persistence
- Complex date of birth input (3 separate fields)
- Long education definitions cluttering the form

### Proposed UX Improvements

Break into **4 logical steps** with pagination, progress bar, and persistence:

| Step | Section | Fields |
|------|---------|--------|
| 1 | Welcome & Eligibility | Event info, attendance confirmation, eligibility checkboxes |
| 2 | Contact Details | First/last name, email, phone, address (line 1, line 2, city, postcode) |
| 3 | About You | Gender, DOB, ethnicity, disability status, NHS satisfaction, education level |
| 4 | Consent & Submit | Data consent checkbox, future contact opt-in, submit button |

### Additional Improvements
- Move education definitions to collapsible/tooltip
- Cleaner DOB input grouping
- Helpful hints and placeholders
- Section context in progress indicator

### Form Fields (from original)

**Eligibility (checkboxes)**
- Can attend all dates
- Is eligible (age 16+, UK resident, received invitation, not excluded roles)

**Contact Details**
- First Name, Last Name
- Email, Phone
- Address Line 1, Address Line 2, City, Post Code

**Demographics**
- Gender (Female, Male, Non-binary/Other)
- Date of Birth (Day, Month, Year)
- Ethnic group (7 options)
- Disability status (3 options)
- NHS satisfaction (5-point scale)
- Highest educational qualification (6 levels with definitions)

**Consent**
- Data use consent (required)
- Stay on database for future events (optional)

---

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## Configuration

### Secret Key
Location: `app.py`
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Debug Mode
Set `debug=False` for production in `app.py`.

## Security Considerations

- Change `app.secret_key` in production
- Set `debug=False` in production
- Add CSRF protection for production use
- Validate and sanitize all user inputs
- Consider rate limiting for production

## Dependencies

- Flask==3.0.0 - Web framework
- Werkzeug==3.0.1 - WSGI utility library
- Alpine.js 3.x (CDN) - Frontend reactivity
- Alpine.js Persist plugin (CDN) - localStorage persistence

## Notes

- This is a POC demonstrating AI-aided form templating
- XML templates serve as structured prompts for implementation
- All client data persists in localStorage until submission
- Server data persists in `data/submissions.json`
