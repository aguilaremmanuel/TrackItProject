document.addEventListener('DOMContentLoaded', function () {
    // PASSWORD EYE TOGGLE
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');

    togglePassword.addEventListener('click', function () {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });

    togglePassword2.addEventListener('click', function () {
        const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
        password2.setAttribute('type', type);
        this.classList.toggle('fa-eye');
        this.classList.toggle('fa-eye-slash');
    });

    /* ROLE OPTION DISABLE ACCORDING TO USER OFFICE */

    const officeDropdown = document.getElementById('selectOffice');
    const roleDropdown = document.getElementById('selectRole');
    const options = roleDropdown.querySelectorAll('option');

    function updateRoleDropdown() {
        const selectedOffice = officeDropdown.value;

        // Show or hide role options based on selected office
        options.forEach(option => {
            if (selectedOffice === 'ADM') {
                if (option.value === 'ADO') {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'none';
                }
            } else if (['ACC', 'BMD', 'CSR', 'PRL'].includes(selectedOffice)) {
                if (['ADO', 'SRO'].includes(option.value)) {
                    option.style.display = 'block';
                } else {
                    option.style.display = 'none';
                }
            } else {
                option.style.display = 'block';
            }
        });

        // Automatically set role and disable role dropdown if 'ADM' is selected
        if (selectedOffice === 'ADM') {
            roleDropdown.value = 'ADO';
        } else {
            roleDropdown.value = '';
        }
    }

    updateRoleDropdown();
    officeDropdown.addEventListener('change', updateRoleDropdown);
});
