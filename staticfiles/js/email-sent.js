document.addEventListener('DOMContentLoaded', function() {
    // Listen for form submission
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        
        // Hide the forgot password form
        // document.getElementById('forgotPasswordForm').classList.add('d-none');
        // document.getElementById('forgotPasswordForm').style.display = 'none';
        // Show the email sent confirmation
        document.getElementById('emailSentConfirmation').classList.remove('d-none');
        // document.getElementById('emailSentConfirmation').style.display = 'block';

    }); 
});