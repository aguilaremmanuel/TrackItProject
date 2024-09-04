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

    // ROLE OPTION HANDLING ACCORDING TO SELECTED OFFICE
    const officeDropdown = document.getElementById('selectOffice');
    const roleDropdown = document.getElementById('selectRole');
    const adminOfficerOption = roleDropdown.querySelector('option[value="ADO"]');

    function updateRoleDropdown() {
        const selectedOffice = officeDropdown.value;

        if (selectedOffice === 'ADM') {
            roleDropdown.value = 'ADO';
            roleDropdown.disabled = true;
            adminOfficerOption.style.display = 'block';
        } else {
            roleDropdown.disabled = false;
            roleDropdown.value = '';
            if (['ACC', 'BMD', 'CSR', 'PRL'].includes(selectedOffice)) {
                adminOfficerOption.style.display = 'none';
            } else {
                adminOfficerOption.style.display = 'block';
            }
        }
    }

    updateRoleDropdown();
    officeDropdown.addEventListener('change', updateRoleDropdown);
});
