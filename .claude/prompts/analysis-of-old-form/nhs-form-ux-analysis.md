# NHS National Conversation Form - UX Analysis & Recommendations

## User Requirements

**Goal**: Build a new application form for a national conversation event on the future of the NHS.

**Approach**:
- Reuse UX solutions from the job assessment form POC (pagination, progress bar, save/persistence)
- Reuse input components introduced in the POC
- Create `form-template-nhs.xml` using the same XML notation as `form-template.xml`
- Implement using the same stack (Flask, Alpine.js, localStorage persistence)

**Source**: Original form in `National conversation on the future of the NHS.html`

---

## UX Analysis of Original Form

### Problems Identified

1. **Single long page** - All fields presented at once, creating an overwhelming wall of content

2. **Dense introductory text** - Important information (dates, compensation, contact details) buried in paragraphs that users may skip

3. **No progress indicator** - Users have no sense of how far along they are or how much remains

4. **No draft persistence** - If the page is closed or refreshed, all entered data is lost

5. **Complex date of birth input** - Split across 3 separate fields (day dropdown, month dropdown, year text input)

6. **Cluttered education section** - Long list of qualification definitions inline with the form field

7. **Poor visual hierarchy** - Checkboxes, selects, and text inputs mixed without clear grouping

8. **No section context** - Headers exist but no indication of overall form structure

---

## Proposed UX Improvements

### Multi-Step Structure

Break the form into **4 logical steps** with clear progression:

| Step | Section | Purpose |
|------|---------|---------|
| 1 | Welcome & Eligibility | Set context, confirm basic requirements |
| 2 | Contact Details | Collect personal and address information |
| 3 | About You | Gather demographic data for lottery selection |
| 4 | Consent & Submit | Legal consent and final submission |

### Step 1: Welcome & Eligibility

**Content**:
- Brief event summary (date, location, compensation)
- Key contact info (Freephone, email)
- Important notes (individual email required, data sharing)

**Fields**:
- Checkbox: "I can attend all dates" (required)
- Checkbox: "I am eligible to attend" (required)

**Rationale**: Gets commitment upfront before collecting personal data. Users who can't attend won't waste time filling the form.

### Step 2: Contact Details

**Fields**:
- First Name (text, required)
- Last Name (text, required)
- Email (email, required)
- Phone (tel, required)
- Address Line 1 (text, required)
- Address Line 2 (text, optional)
- City (text, required)
- Post Code (text, required)

**Rationale**: Groups all contact/address info together. Logical flow from name to contact to location.

### Step 3: About You

**Fields**:
- Gender (select, required)
- Date of Birth - Day (select, required)
- Date of Birth - Month (select, required)
- Date of Birth - Year (text, required)
- Ethnic Group (select, required)
- Disability Status (select, required)
- NHS Satisfaction (select, required)
- Educational Qualification (select, required)

**Improvements**:
- Group DOB fields visually with shared label
- Move education definitions to tooltip/collapsible (not inline)
- Add helper text explaining why demographics are collected

**Rationale**: All demographic/lottery selection data together. Explains purpose to reduce friction on sensitive questions.

### Step 4: Consent & Submit

**Fields**:
- Checkbox: "I consent to the use of my data..." (required)
- Checkbox: "Please inform me of similar events..." (optional)

**Content**:
- Summary of what happens next
- Link to privacy policy

**Rationale**: Clear final step with legal requirements. Optional marketing opt-in separated from required consent.

---

## Additional UX Enhancements

### Progress Indicator
- Show "Step X of 4: Section Name"
- Visual progress bar with percentage
- Step labels (clickable to navigate back?)

### Persistence
- Auto-save to localStorage on every field change
- "Clear Draft" button to start over
- Clear localStorage on successful submission

### Help & Guidance
- Placeholders with example formats
- Helper text for complex fields
- Tooltips for definitions (education levels)

### Validation
- Client-side HTML5 validation
- Server-side validation with clear error messages
- Inline validation feedback

### Mobile Responsiveness
- Touch-friendly inputs
- Adequate spacing between fields
- Readable text sizes

---

## Field Reference

### Select Field Options

**Gender**:
- Female (value: 2)
- Male (value: 1)
- Non-binary or Other (value: 3)

**Day**: 1-31

**Month**: January-December (values: 1-12)

**Ethnic Group**:
- Asian or Asian British (value: 3)
- Black, African, Caribbean or Black British (value: 4)
- Mixed or Multiple ethnic groups (value: 2)
- White English, Welsh, Scottish, Northern Irish or British (value: 1)
- White Irish (value: 7)
- White other (value: 6)
- Other ethnic group (value: 5)

**Disability Status**:
- Yes, limited a little (value: 2)
- Yes, limited a lot (value: 1)
- No (value: 3)

**NHS Satisfaction**:
- Very satisfied (value: 1)
- Quite satisfied (value: 2)
- Neither satisfied nor dissatisfied (value: 3)
- Quite dissatisfied (value: 4)
- Very dissatisfied (value: 5)

**Educational Qualification**:
- No qualifications, or none yet (value: 1)
- Level 1 (value: 2)
- Level 2 (value: 3)
- Level 3 (value: 4)
- Level 4 or above (value: 5)
- Apprenticeship, or other qualification (value: 6)

### Education Level Definitions

For tooltip/collapsible content:

- **No qualifications**: None of the qualifications listed below
- **Level 1**: Up to 4 GCSEs (A*-C), any GCSEs/O levels/CSEs at other grades, 1 AS level, NVQ level 1
- **Level 2**: 5+ GCSEs (A*-C), O levels, CSEs; 1 A level; 2-3 AS levels; Welsh Baccalaureate Intermediate; NVQ level 2; BTEC First/General Diploma
- **Level 3**: 2+ A levels; 4+ AS levels; Higher School Certificate; Welsh Baccalaureate Advanced; NVQ level 3; BTEC National
- **Level 4+**: Degree (BA, BSc); higher degree (MA, PhD, PGCE); NVQ level 4-5; BTEC Higher; professional qualifications
- **Apprenticeship/Other**: Apprenticeship; vocational/work-related qualifications; other qualifications

---

## Next Steps

1. Create `form-template-nhs.xml` using the agreed structure
2. Implement Flask backend with appropriate routes and validation
3. Build Alpine.js frontend with persistence
4. Style consistently with POC
5. Test multi-step flow and persistence
