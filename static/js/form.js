/**
 * NHS Conversation Registration Form - JavaScript
 * Handles form state management and persistence using Alpine.js
 */

// Constants
const STORAGE_KEY = 'nhsConversationDraft';
const ALPINE_STORAGE_KEY = `_x_${STORAGE_KEY}`;

// Default form data structure
function getDefaultFormData() {
    return {
        canAttend: false,
        isEligible: false,
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address1: '',
        address2: '',
        city: '',
        postCode: '',
        gender: '',
        dobDay: '',
        dobMonth: '',
        dobYear: '',
        ethnicity: '',
        disability: '',
        nhsSatisfaction: '',
        education: '',
        dataConsent: false,
        futureContact: false
    };
}

// Alpine.js form data component
function createFormData(csrfToken) {
    return {
        // CSRF token should NOT be persisted - always use fresh token from server
        csrfToken: csrfToken,
        currentStep: 1,
        totalSteps: 4,
        stepNames: ['Welcome & Eligibility', 'Contact Details', 'About You', 'Consent & Submit'],

        // Form data object - will be persisted via Alpine Persist plugin
        formData: null,

        init() {
            // Initialize formData with Alpine's $persist
            // This ensures only formData is persisted, not csrfToken
            if (!this.formData || Object.keys(this.formData).length === 0) {
                this.formData = getDefaultFormData();
            }
        },

        getDefaultFormData() {
            return getDefaultFormData();
        },

        clearDraft() {
            this.formData = getDefaultFormData();
            this.currentStep = 1;
        }
    };
}

// Utility: Clear form draft from localStorage (used on success page)
function clearFormDraft() {
    localStorage.removeItem(ALPINE_STORAGE_KEY);
}

// Export for global access
window.createFormData = createFormData;
window.clearFormDraft = clearFormDraft;
