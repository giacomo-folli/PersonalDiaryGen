// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Set the month and year to the current month/year
    const now = new Date();
    if (document.getElementById('month')) {
        document.getElementById('month').value = now.getMonth() + 1; // Months are 0-indexed in JS
    }
    if (document.getElementById('year')) {
        document.getElementById('year').value = now.getFullYear();
    }

    // Add event listener to the diary form
    const diaryForm = document.getElementById('diary-form');
    if (diaryForm) {
        diaryForm.addEventListener('submit', function(e) {
            // Show loading indicator
            const submitBtn = diaryForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';
            
            // Let the form submission continue naturally
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Function to preview the diary
function previewDiary() {
    const month = document.getElementById('month').value;
    const year = document.getElementById('year').value;
    
    // Validate month and year
    if (!month || !year) {
        alert('Please select both month and year');
        return;
    }
    
    // Get the month name
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const monthName = monthNames[month - 1];
    
    // Show a simple preview modal
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    document.getElementById('previewMonthYear').textContent = `${monthName} ${year}`;
    previewModal.show();
}

// Function to handle login form validation
function validateLoginForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        alert('Please enter both username and password');
        return false;
    }
    
    return true;
}

// Function to handle signup form validation
function validateSignupForm() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (!username || !email || !password || !confirmPassword) {
        alert('Please fill out all fields');
        return false;
    }
    
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return false;
    }
    
    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return false;
    }
    
    return true;
}
