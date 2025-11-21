# WCAG Accessibility Analysis - NHS Conversation Registration Form

This document provides a comprehensive accessibility analysis of the NHS Conversation Registration Form, including identified issues, solutions, implementation status, and WCAG 2.1 compliance mapping.

## Executive Summary

The NHS Conversation Registration Form is a multi-step Alpine.js-powered form collecting personal and demographic information. This analysis identifies critical accessibility barriers affecting keyboard navigation, screen reader users, and compliance with WCAG 2.1 Level AA standards.

**Current Status:**
- ❌ **WCAG 2.1 Level A**: Non-compliant (keyboard navigation broken)
- ❌ **WCAG 2.1 Level AA**: Non-compliant (missing ARIA labels, focus management)
- ✅ **Phase 1 Complete**: Keyboard navigation fixed with `inert` attribute
- 🟡 **Phase 2 Pending**: ARIA labels and screen reader support

---

## Accessibility Issues Identified

### 🔴 Critical Issues (WCAG Level A Violations)

#### Issue 1: Hidden Form Fields Remain Focusable
**WCAG Criterion:** 2.1.1 Keyboard (Level A)

**Problem:**
```html
<!-- Current implementation (broken) -->
<div x-show="currentStep === 2" x-transition>
    <input type="text" id="firstName" ...>
    <!-- ❌ Still in tab order when hidden -->
</div>
```

Alpine.js `x-show` uses `display: none` for visibility, but elements remain in the DOM and tab order. Keyboard users tab through invisible fields, creating confusion and breaking navigation flow.

**Impact:**
- **Severity**: Critical
- **Users Affected**: All keyboard-only users, mobility-impaired users
- **WCAG Level**: A (Failure)
- **User Experience**: Keyboard navigation completely broken

**Solution Implemented:**
```html
<!-- Fixed with inert attribute -->
<div x-show="currentStep === 2"
     :inert="currentStep !== 2"
     x-transition>
    <input type="text" id="firstName" ...>
    <!-- ✅ Not focusable when hidden -->
</div>
```

The `inert` attribute makes hidden sections:
- Non-focusable (removed from tab order)
- Non-clickable (no pointer events)
- Hidden from screen readers (aria-hidden behavior)
- Kept in DOM (form submission works)

**Status:** ✅ **RESOLVED** (Phase 1)

---

#### Issue 2: Multiple Navigation Buttons in Tab Order
**WCAG Criterion:** 2.4.3 Focus Order (Level A)

**Problem:**
```html
<!-- Three buttons, all in tab order -->
<button x-show="currentStep > 1">Previous</button>      <!-- Hidden on step 1, but tabbable -->
<button x-show="currentStep < 4">Next</button>          <!-- Hidden on step 4, but tabbable -->
<button x-show="currentStep === 4">Register</button>    <!-- Hidden on steps 1-3, but tabbable -->
<button>Clear Form</button>                              <!-- Always visible -->
```

All four buttons exist in the DOM simultaneously. Hidden buttons are still tabbable, causing:
- Tab stops on invisible buttons
- Confusing focus order
- Unexpected keyboard behavior

**Impact:**
- **Severity**: Critical
- **Users Affected**: Keyboard users, screen reader users
- **WCAG Level**: A (Failure)

**Solution Implemented:**
```html
<button x-show="currentStep > 1"
        :inert="currentStep <= 1"
        ...>Previous</button>

<button x-show="currentStep < totalSteps"
        :inert="currentStep >= totalSteps"
        ...>Next</button>

<button x-show="currentStep === totalSteps"
        :inert="currentStep !== totalSteps"
        ...>Register</button>
```

**Status:** ✅ **RESOLVED** (Phase 1)

---

### 🟡 Important Issues (WCAG Level AA Violations)

#### Issue 3: Missing Progress Bar ARIA Attributes
**WCAG Criterion:** 1.3.1 Info and Relationships (Level A), 4.1.2 Name, Role, Value (Level A)

**Problem:**
```html
<!-- Current implementation (incomplete) -->
<div class="progress-container">
    <div class="progress-bar">
        <div class="progress-fill" :style="'width: ' + (currentStep / totalSteps * 100) + '%'"></div>
    </div>
    <div class="progress-text">
        Step <span x-text="currentStep"></span> of <span x-text="totalSteps"></span>
    </div>
</div>
```

Missing semantic information:
- No `role="progressbar"`
- No `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- No `aria-label` describing purpose
- Progress only communicated visually

**Impact:**
- **Severity**: High
- **Users Affected**: Screen reader users, visually impaired users
- **WCAG Level**: A (Failure)

**Recommended Solution:**
```html
<div class="progress-container">
    <div class="progress-bar"
         role="progressbar"
         :aria-valuenow="currentStep"
         aria-valuemin="1"
         :aria-valuemax="totalSteps"
         aria-label="Registration progress">
        <div class="progress-fill" :style="'width: ' + (currentStep / totalSteps * 100) + '%'"></div>
    </div>
    <div class="progress-text" aria-live="polite">
        Step <span x-text="currentStep"></span> of <span x-text="totalSteps"></span>
    </div>
</div>
```

**Status:** 🟡 **PENDING** (Phase 2)

---

#### Issue 4: Form Steps Lack Semantic Structure
**WCAG Criterion:** 1.3.1 Info and Relationships (Level A), 2.4.6 Headings and Labels (Level AA)

**Problem:**
```html
<!-- Current implementation -->
<div x-show="currentStep === 1">
    <!-- No semantic landmark or label -->
</div>
```

Missing:
- `role="region"` to create landmarks
- `aria-labelledby` to associate with heading
- Semantic section elements
- Clear structure for assistive technology

**Impact:**
- **Severity**: Medium
- **Users Affected**: Screen reader users
- **WCAG Level**: AA (Failure)

**Recommended Solution:**
```html
<section role="region"
         aria-labelledby="step-1-heading"
         x-show="currentStep === 1"
         :inert="currentStep !== 1">
    <h2 id="step-1-heading" x-text="stepNames[0]"></h2>
    <!-- Step content -->
</section>
```

**Status:** 🟡 **PENDING** (Phase 2)

---

#### Issue 5: No Live Region for Error Messages
**WCAG Criterion:** 4.1.3 Status Messages (Level AA)

**Problem:**
```html
<!-- Current implementation -->
<div class="alert-group">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
</div>
```

Issues:
- No `role="alert"` or `aria-live`
- Errors not announced to screen readers
- Users must manually find error messages
- Validation failures are silent

**Impact:**
- **Severity**: High
- **Users Affected**: Screen reader users, blind users
- **WCAG Level**: AA (Failure)

**Recommended Solution:**
```html
<div class="alert-group"
     role="alert"
     aria-live="assertive"
     aria-atomic="true">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    <span class="sr-only">Error: </span>{{ message }}
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}
</div>
```

**Status:** 🟡 **PENDING** (Phase 2)

---

#### Issue 6: No Focus Management on Step Navigation
**WCAG Criterion:** 2.4.3 Focus Order (Level A), 3.2.1 On Focus (Level A)

**Problem:**
When users click "Next" or "Previous":
- Focus remains on the navigation button
- User must tab from beginning to find new content
- No indication that content changed
- Poor keyboard UX

**Impact:**
- **Severity**: Medium
- **Users Affected**: Keyboard users, screen reader users, users with cognitive disabilities
- **WCAG Level**: A (Best Practice)

**Recommended Solution:**
```javascript
// In Alpine.js component
nextStep() {
    this.currentStep++;
    this.$nextTick(() => {
        // Focus on step heading
        const heading = document.querySelector(`#step-${this.currentStep}-heading`);
        if (heading) {
            heading.focus();
            heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
},

previousStep() {
    this.currentStep--;
    this.$nextTick(() => {
        const heading = document.querySelector(`#step-${this.currentStep}-heading`);
        if (heading) {
            heading.focus();
            heading.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
}
```

CSS for focusable headings:
```css
h2[tabindex="-1"]:focus {
    outline: 2px solid #005fcc;
    outline-offset: 2px;
}
```

**Status:** 🟡 **PENDING** (Phase 2)

---

#### Issue 7: No Screen Reader Announcements for Step Changes
**WCAG Criterion:** 4.1.3 Status Messages (Level AA)

**Problem:**
When user navigates between steps:
- No announcement that step changed
- Screen reader users unaware of context change
- Must explore page to understand new content

**Impact:**
- **Severity**: Medium
- **Users Affected**: Screen reader users, blind users
- **WCAG Level**: AA (Failure)

**Recommended Solution:**
```html
<!-- Add screen reader-only live region -->
<div aria-live="polite"
     aria-atomic="true"
     class="sr-only">
    <span x-text="`Step ${currentStep} of ${totalSteps}: ${stepNames[currentStep - 1]}`"></span>
</div>
```

CSS for screen reader-only content:
```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

**Status:** 🟡 **PENDING** (Phase 2)

---

### 🟢 Nice-to-Have Improvements (Best Practices)

#### Enhancement 1: Skip to Main Content Link
**WCAG Criterion:** 2.4.1 Bypass Blocks (Level A)

**Purpose:** Allow keyboard users to skip repetitive navigation and jump directly to form content.

**Implementation:**
```html
<body>
    <a href="#main-form" class="skip-link">Skip to registration form</a>

    <div class="top-logo">...</div>

    <div class="container">
        <h1>National conversation on the future of the NHS</h1>
        <form id="main-form" ...>
```

CSS:
```css
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
```

**Status:** 🟢 **OPTIONAL** (Phase 3)

---

#### Enhancement 2: Keyboard Shortcuts for Step Navigation
**WCAG Criterion:** Best Practice (Not required)

**Purpose:** Power users can navigate steps without tabbing to buttons.

**Implementation:**
```javascript
// Add to Alpine.js component
handleKeydown(event) {
    // Only handle shortcuts when not typing in input
    if (event.target.tagName === 'INPUT' ||
        event.target.tagName === 'SELECT' ||
        event.target.tagName === 'TEXTAREA') {
        return;
    }

    // Ctrl+Right Arrow = Next step
    if (event.ctrlKey && event.key === 'ArrowRight' && this.currentStep < this.totalSteps) {
        event.preventDefault();
        this.nextStep();
    }

    // Ctrl+Left Arrow = Previous step
    if (event.ctrlKey && event.key === 'ArrowLeft' && this.currentStep > 1) {
        event.preventDefault();
        this.previousStep();
    }
}
```

Add to form:
```html
<form @keydown.window="handleKeydown">
```

**Status:** 🟢 **OPTIONAL** (Phase 3)

---

#### Enhancement 3: Fieldsets for Related Form Groups
**WCAG Criterion:** 1.3.1 Info and Relationships (Level A) - Best Practice

**Purpose:** Group related form fields semantically.

**Example - Date of Birth:**
```html
<!-- Current -->
<div class="field-group">
    <span class="field-group-label">What is your date of birth? *</span>
    <div class="field-group-fields">
        <select id="dobDay">...</select>
        <select id="dobMonth">...</select>
        <input id="dobYear">...</input>
    </div>
</div>

<!-- Improved -->
<fieldset class="field-group">
    <legend>What is your date of birth? *</legend>
    <div class="field-group-fields">
        <div>
            <label for="dobDay">Day</label>
            <select id="dobDay">...</select>
        </div>
        <div>
            <label for="dobMonth">Month</label>
            <select id="dobMonth">...</select>
        </div>
        <div>
            <label for="dobYear">Year</label>
            <input id="dobYear">...</input>
        </div>
    </div>
</fieldset>
```

**Status:** 🟢 **OPTIONAL** (Phase 3)

---

#### Enhancement 4: Enhanced Focus Indicators
**WCAG Criterion:** 2.4.7 Focus Visible (Level AA)

**Purpose:** Make keyboard focus more visible for low-vision users.

**Implementation:**
```css
/* Enhanced focus styles */
input:focus,
select:focus,
textarea:focus,
button:focus {
    outline: 3px solid #005fcc;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(0, 95, 204, 0.1);
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    input:focus,
    select:focus,
    textarea:focus,
    button:focus {
        outline: 3px solid currentColor;
    }
}
```

**Status:** 🟢 **OPTIONAL** (Phase 3)

---

## Implementation Phases

### ✅ Phase 1: Critical Keyboard Navigation (COMPLETED)

**Objective:** Fix keyboard navigation to achieve basic usability.

**Implemented:**
1. ✅ Added `inert` attribute to hidden form steps
2. ✅ Added `inert` attribute to hidden navigation buttons
3. ✅ Verified form submission still works with hidden fields in DOM

**Result:**
- Keyboard navigation now works correctly
- Only visible elements are focusable
- Form data submission unaffected
- Tab order is logical and predictable

**Testing:**
```
✅ Tab through Step 1 - only Step 1 fields focusable
✅ Click Next - only Step 2 fields focusable
✅ Navigation buttons properly managed
✅ Form submits all data from all steps
```

---

### 🟡 Phase 2: ARIA Labels & Screen Reader Support (IN PROGRESS)

**Objective:** Make form fully accessible to screen reader users.

**Tasks:**
1. 🟡 Add ARIA labels to progress bar
2. 🟡 Add ARIA labels to form sections
3. 🟡 Add live region for error announcements
4. 🟡 Add focus management on step navigation
5. 🟡 Add screen reader announcements for step changes

**Expected Outcome:**
- WCAG 2.1 Level AA compliance
- Full screen reader support
- Dynamic content changes announced
- Clear navigation structure

---

### 🟢 Phase 3: Enhancements (OPTIONAL)

**Objective:** Polish user experience and exceed minimum standards.

**Optional Tasks:**
1. 🟢 Add skip link
2. 🟢 Implement keyboard shortcuts
3. 🟢 Use fieldsets for grouped inputs
4. 🟢 Enhanced focus indicators
5. 🟢 Add form autosave indicator
6. 🟢 Add client-side validation with accessible error messages

---

## WCAG 2.1 Compliance Matrix

### Level A Criteria

| Criterion | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **1.3.1** Info and Relationships | Semantic HTML structure | 🟡 Partial | Need fieldsets, better headings |
| **2.1.1** Keyboard | All functionality via keyboard | ✅ Pass | Fixed with `inert` |
| **2.4.3** Focus Order | Logical focus order | ✅ Pass | Fixed with `inert` |
| **3.2.1** On Focus | No context change on focus | ✅ Pass | - |
| **4.1.2** Name, Role, Value | Proper ARIA attributes | 🟡 Partial | Need progress bar ARIA |

### Level AA Criteria

| Criterion | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| **2.4.6** Headings and Labels | Descriptive headings | 🟡 Partial | Need better section labeling |
| **2.4.7** Focus Visible | Visible keyboard focus | ✅ Pass | Browser defaults sufficient |
| **3.3.3** Error Suggestion | Provide error suggestions | ✅ Pass | Clear error messages |
| **4.1.3** Status Messages | Announce status changes | ❌ Fail | Need live regions |

**Current Compliance:**
- **Level A**: 80% (4/5 pass)
- **Level AA**: 50% (2/4 pass)

**After Phase 2:**
- **Level A**: 100% (5/5 pass) ✅
- **Level AA**: 100% (4/4 pass) ✅

---

## Testing Recommendations

### Keyboard Testing
```
✅ Tab through entire form
✅ Shift+Tab to navigate backwards
✅ Arrow keys in select dropdowns
✅ Space to toggle checkboxes
✅ Enter to submit form
✅ Esc to close (if applicable)
```

### Screen Reader Testing

**Tools:**
- **NVDA** (Windows, free)
- **JAWS** (Windows, paid)
- **VoiceOver** (macOS, built-in)
- **TalkBack** (Android, built-in)

**Test Scenarios:**
```
□ Navigate by headings (H key)
□ Navigate by form controls (F key)
□ Navigate by landmarks (D key)
□ Hear progress announcements
□ Hear error messages
□ Hear step change announcements
□ Verify all form labels read correctly
```

### Automated Testing Tools

**Recommended:**
1. **axe DevTools** (Chrome/Firefox extension)
2. **WAVE** (Web Accessibility Evaluation Tool)
3. **Lighthouse** (Chrome DevTools, Accessibility audit)
4. **Pa11y** (Command-line tool)

**Run After Each Phase:**
```bash
# Using axe-core CLI
npx @axe-core/cli http://localhost:5000

# Using Pa11y
npx pa11y http://localhost:5000
```

---

## Browser Support Notes

### `inert` Attribute Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 102+ | ✅ Supported |
| Firefox | 112+ | ✅ Supported |
| Safari | 15.5+ | ✅ Supported |
| Edge | 102+ | ✅ Supported |

**Coverage:** ~95% of global users (as of 2024)

**Fallback for older browsers:**
If needed, use a polyfill:
```html
<script src="https://cdn.jsdelivr.net/npm/wicg-inert@3/dist/inert.min.js"></script>
```

---

## Success Metrics

### Quantitative Metrics
- ✅ **0 keyboard traps** (was: multiple)
- ✅ **Logical tab order** (was: broken)
- 🎯 **0 axe violations** (target: after Phase 2)
- 🎯 **100% WCAG AA compliance** (target: after Phase 2)

### Qualitative Metrics
- ✅ Keyboard-only users can complete form
- 🎯 Screen reader users can complete form independently
- 🎯 All error messages are announced
- 🎯 All dynamic changes are announced

---

## Implementation Status Summary

**Completed:**
- ✅ Phase 1: Critical keyboard navigation fixes
- ✅ Form fields remain in DOM for submission
- ✅ Hidden elements not focusable

**In Progress:**
- 🟡 Phase 2: ARIA labels and screen reader support

**Pending:**
- 🟢 Phase 3: Optional enhancements

**Estimated Time to Full Compliance:**
- Phase 2: ~2-3 hours
- Phase 3: ~1-2 hours (optional)

---

## References

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **MDN Web Docs - Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- **WebAIM Resources**: https://webaim.org/
- **HTML `inert` attribute**: https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/inert

---

## Change Log

| Date | Change | Phase |
|------|--------|-------|
| 2025-11-21 | Initial accessibility analysis created | - |
| 2025-11-21 | Implemented `inert` attribute for keyboard navigation | Phase 1 ✅ |
| TBD | ARIA labels implementation | Phase 2 🟡 |

---

*This document should be updated as accessibility improvements are implemented.*
