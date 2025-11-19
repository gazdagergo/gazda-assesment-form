# AI-Aided Templating (DSL) - Conversation Log

## Concept

After exploring various templating and component solutions (Jinja2 macros, Chameleon), the user proposed a novel approach: **AI-aided templating**.

## What is AI-Aided Templating?

Instead of using traditional template libraries, rely on Claude to understand patterns and similarities. The approach uses a **Domain-Specific Language (DSL)** in XML format that:

1. Describes structure and logic declaratively
2. Uses natural language prompts as parameters where needed
3. Acts as a "source of truth" that Claude interprets to generate actual code
4. Makes modifications easier - just change the pseudo code

## How It Works

1. **Create XML representation** - Describes the form structure, fields, validation, and logic
2. **Include logic prompts** - Natural language descriptions of behavior
3. **AI interprets** - Claude reads the XML and generates/modifies Flask + Jinja2 + Alpine.js code

## Pros

- Extremely readable and maintainable
- Tech-stack agnostic - describes WHAT, not HOW
- Natural language for complex logic
- Easy for non-developers to understand
- Single source of truth
- No need for complex template library syntax

## Cons

- Requires AI interpretation each time
- Need to ensure prompts are unambiguous
- No direct execution - always needs AI translation

---

## Implementation

Created `form-template.xml` with the following structure:

```xml
<Form title="..." action="/submit" method="POST">

    <!-- Global State Management -->
    <State persist="true" storageKey="jobApplicationDraft">
        <Field name="name" default="" />
        ...
    </State>

    <!-- Pagination Logic -->
    <Pagination totalSteps="2">
        <ProgressIndicator logic="Shows step labels with bold..." />
    </Pagination>

    <!-- Form Sections -->
    <FormSection step="1" title="Personal Information">
        <FormField
            name="name"
            label="Full Name"
            type="text"
            required="true"
            model="formData.name"
            logic="Binds to persisted state. Validates on server..." />
        ...
    </FormSection>

    <!-- Navigation -->
    <Navigation>
        <NextButton label="Next" logic="Shows only when not on last step..." />
        <SubmitButton label="Submit Application" logic="Shows only on last step..." />
        ...
    </Navigation>

</Form>
```

---

## Usage Examples

### Adding a New Field

Add to XML:
```xml
<FormField
    name="linkedin"
    label="LinkedIn Profile"
    type="url"
    required="false"
    placeholder="https://linkedin.com/in/yourprofile"
    model="formData.linkedin"
    logic="Optional field. Binds to persisted state." />
```

Then tell Claude: "Update the implementation to match form-template.xml"

### Changing Validation

Modify the `logic` attribute:
```xml
logic="Validates on server: must be valid URL format. Show error if invalid."
```

### Adding a New Step

1. Add `<FormSection step="3" title="Additional Info">...</FormSection>`
2. Update `<Pagination totalSteps="3">`

---

## The Pattern

This is essentially **prompt-driven development**:
- XML is a structured prompt
- Claude consistently interprets it
- Generates implementation in the target tech stack

The XML acts as a **contract** between the developer and the AI - a clear, unambiguous specification that Claude can reliably translate into working code.

---

## Files Created

- `form-template.xml` - The AI-aided template / DSL representation of the form
