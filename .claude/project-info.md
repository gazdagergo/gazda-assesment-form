# Form Assessment System - Project Information

## Project Overview

This project demonstrates an **AI-aided form templating approach** using a declarative XML schema to define forms, which are then implemented as Flask/Alpine.js web applications.

**Current forms:**
- **Job Assessment Form** (POC) - 2-step form for job applications
- **NHS National Conversation Form** - 4-step registration form for national event

## Technology Stack

- **Backend**: Python 3.x with Flask 3.0.0
- **Frontend**: HTML5, CSS3, Alpine.js 3.x with Persist plugin
- **Storage**: JSON file-based storage (server), localStorage (client drafts)
- **Template Engine**: Jinja2 (built into Flask)
- **Form Definition**: Custom XML DSL in `prompt-templates/`

## Project Structure

```
gazda-assesment-form/
├── .claude/
│   ├── project-info.md              # This file - project documentation
│   └── prompts/
│       └── analysis-of-old-form/    # NHS form analysis
│           ├── National conversation on the future of the NHS.html
│           └── nhs-form-ux-analysis.md
├── prompt-templates/                # XML form definitions (AI prompts)
│   ├── form-template.xml            # Job assessment form schema
│   └── form-template-nhs.xml        # NHS conversation form schema
├── app.py                           # Flask app - Job assessment form
├── app_nhs.py                       # Flask app - NHS conversation form
├── requirements.txt                 # Python dependencies
├── README.md                        # Setup instructions
├── data/
│   ├── submissions.json             # Job form submissions
│   └── nhs_submissions.json         # NHS form submissions
├── templates/
│   ├── form.html                    # Job assessment form (Alpine.js)
│   ├── form_nhs.html                # NHS conversation form (Alpine.js)
│   ├── success.html                 # Job form success page
│   └── success_nhs.html             # NHS form success page
└── static/
    └── css/
        └── style.css                # Shared application styles
```

---

## AI-Aided Templating Approach

### What are Prompt Templates?

The `prompt-templates/` directory contains **declarative XML files** that serve a dual purpose:

1. **Structured Documentation** - Human-readable specification of form structure, fields, validation rules, and UX behavior
2. **AI Prompts** - Machine-interpretable blueprints that Claude can use to generate or modify working implementations

This approach separates the "what" (XML schema) from the "how" (Flask/Alpine.js code), making it easier to:
- Design forms at a high level without implementation details
- Generate consistent implementations from templates
- Modify forms by updating the XML and regenerating code
- Maintain documentation that stays in sync with implementation

### How It Works

1. **Define** - Create an XML template describing form structure, fields, validation, and behavior
2. **Prompt** - Use the XML as context when asking Claude to implement or modify the form
3. **Generate** - Claude produces Flask routes, HTML templates, and Alpine.js code following the schema
4. **Iterate** - Update XML and regenerate to make changes

### XML Schema Reference

#### Root Element
```xml
<Form title="..." subtitle="..." action="/submit" method="POST" novalidate="true">
```

#### State Management
Defines fields persisted to localStorage via Alpine.js `$persist`:
```xml
<State persist="true" storageKey="draftKeyName">
  <Field name="fieldName" default="" />
  <Field name="checkboxField" default="false" />
</State>
```

#### Pagination
```xml
<Pagination totalSteps="N">
  <ProgressIndicator logic="Description of progress display behavior" />
</Pagination>
```

#### Form Sections
```xml
<FormSection step="1" title="Section Title">
  <!-- fields go here -->
</FormSection>
```

#### Field Types

**Text Input:**
```xml
<FormField
    name="fieldName"
    label="Display Label"
    type="text|email|tel"
    required="true"
    minlength="2"
    placeholder="Placeholder text"
    model="formData.fieldName"
    logic="Description of field behavior" />
```

**Select Dropdown:**
```xml
<SelectField
    name="fieldName"
    label="Display Label"
    required="true"
    model="formData.fieldName"
    defaultOption="Please select...">
    <Option value="1">Option Label</Option>
</SelectField>
```

**Textarea:**
```xml
<TextareaField
    name="fieldName"
    label="Display Label"
    rows="5"
    required="false"
    model="formData.fieldName" />
```

**Checkbox:**
```xml
<CheckboxField
    name="fieldName"
    label="Checkbox label text"
    required="true"
    model="formData.fieldName"
    helpText="Additional explanation" />
```

**Field Group (for related fields like DOB):**
```xml
<FieldGroup label="Group Label">
  <!-- Multiple fields displayed together -->
</FieldGroup>
```

#### Content Elements
```xml
<IntroText>
  <Paragraph>Text content</Paragraph>
  <List>
    <Item>List item</Item>
  </List>
</IntroText>

<SectionIntro>Helper text for the section</SectionIntro>
<DataSharingNotice>Legal notice about data</DataSharingNotice>
```

#### Navigation
```xml
<Navigation>
  <PreviousButton label="Previous" />
  <NextButton label="Next" styling="primary coloring" />
  <SubmitButton label="Submit" styling="primary coloring" />
  <ClearButton label="Clear Form" />
</Navigation>
```

#### Success Behavior
```xml
<OnSuccess redirect="/success" logic="Clear localStorage on success page load" />
```

### Common Attributes

| Attribute | Purpose |
|-----------|---------|
| `name` | Form field name for submission |
| `label` | Display label |
| `model` | Alpine.js x-model binding (e.g., `formData.fieldName`) |
| `required` | Validation requirement (true/false) |
| `placeholder` | Input placeholder text |
| `logic` | Documentation of behavior (not rendered) |
| `helpText` | Additional guidance shown to user |
| `helpContent` | Tooltip/collapsible content |

---

## Implementation Patterns

### Alpine.js State Management

```javascript
x-data="{
  currentStep: 1,
  totalSteps: 4,
  formData: $persist({
    field1: '',
    field2: '',
    checkbox1: false
  }).as('storageKey'),
  clearDraft() {
    this.formData = { field1: '', field2: '', checkbox1: false };
    this.currentStep = 1;
  },
  stepNames: ['Step 1', 'Step 2', 'Step 3', 'Step 4']
}"
```

### Multi-Step Pagination

- Controlled via `currentStep` state variable (1-indexed)
- Each section wrapped in `<div x-show="currentStep === N" x-transition>`
- Navigation buttons conditionally rendered based on step:
  - Previous: `x-show="currentStep > 1"`
  - Next: `x-show="currentStep < totalSteps"`
  - Submit: `x-show="currentStep === totalSteps"`

### Progress Bar

- Visual indicator with percentage width: `(currentStep / totalSteps * 100)%`
- Step labels with dynamic bold styling for current step
- CSS transition for smooth animation
- Text display: "Step X of N"

### Persistence

- **Client-side**: Alpine.js `$persist()` auto-saves to localStorage on every change
- **Server-side**: Flask saves submissions to JSON file with ID and timestamp
- **On success**: localStorage cleared via `localStorage.removeItem('_x_storageKey')`

### Validation

- **Client-side**: HTML5 attributes (required, minlength, type, maxlength)
- **Server-side**: Flask validation in `/submit` route with comprehensive checks
- **Errors**: Flask flash messages displayed at top of form

---

## Form Implementations

### Job Assessment Form (POC)

**Files:**
- `app.py` - Flask backend (port 5000)
- `templates/form.html` - Form template
- `templates/success.html` - Success page
- `prompt-templates/form-template.xml` - Schema

**Steps:**
1. Personal Information (name, email, phone)
2. Professional Details (position, experience, skills)

**Storage:** `data/submissions.json`

**Run:** `python app.py` → http://localhost:5000

---

### NHS National Conversation Form

**Files:**
- `app_nhs.py` - Flask backend (port 5001)
- `templates/form_nhs.html` - Form template
- `templates/success_nhs.html` - Success page
- `prompt-templates/form-template-nhs.xml` - Schema

**Steps:**
1. **Welcome & Eligibility** - Event info, attendance/eligibility confirmations
2. **Contact Details** - Name, email, phone, full address
3. **About You** - Demographics for lottery selection (gender, DOB, ethnicity, disability, NHS satisfaction, education)
4. **Consent & Submit** - Data consent, future contact opt-in

**Storage:** `data/nhs_submissions.json`

**Run:** `python app_nhs.py` → http://localhost:5001

**Features:**
- 20 form fields with full validation
- localStorage persistence with `nhsConversationDraft` key
- Progress indicator with step names
- Education level tooltip
- Data sharing notice with Thinks link
- Withdrawal notice with contact email

---

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Job Assessment Form (POC)
python app.py

# Run NHS Conversation Form
python app_nhs.py
```

## Configuration

### Secret Keys
Each app has its own secret key in the app file:
```python
app.secret_key = 'change-this-in-production'
```

### Ports
- Job Assessment Form: 5000
- NHS Conversation Form: 5001

### Debug Mode
Set `debug=False` for production in both app files.

## Security Considerations

- Change `app.secret_key` values in production
- Set `debug=False` in production
- Add CSRF protection for production use
- Validate and sanitize all user inputs
- Consider adding rate limiting
- Review data retention policies for GDPR compliance

## Dependencies

- Flask==3.0.0 - Web framework
- Werkzeug==3.0.1 - WSGI utility library
- Alpine.js 3.x (CDN) - Frontend reactivity
- Alpine.js Persist plugin (CDN) - localStorage persistence

## Notes

- XML templates in `prompt-templates/` serve as both documentation and AI prompts
- All client data persists in localStorage until successful submission
- Server data persists in `data/*.json` files
- Forms share CSS styles but have independent Flask apps
- Each form can run simultaneously on different ports
