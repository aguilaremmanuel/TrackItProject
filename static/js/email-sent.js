document.getElementById('sendInstructionsBtn').addEventListener('click', function() {
    // Hide the forgot password form
    document.getElementById('forgotPasswordForm').classList.add('d-none');
    // Show the email sent confirmation
    document.getElementById('emailSentConfirmation').classList.remove('d-none');
});