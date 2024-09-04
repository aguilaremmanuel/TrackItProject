document.addEventListener('DOMContentLoaded', function () {
    
    /* PASSWORD EYE TOGGLE */
    
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
    const adminOfficerOption = roleDropdown.querySelector('option[value="ADO"]');

    
    updateRoleDropdown();

    officeDropdown.addEventListener('change', updateRoleDropdown);

    function updateRoleDropdown() {
        
        
        if (officeDropdown.value === 'ADM') {
            roleDropdown.value = 'ADO';
            roleDropdown.disabled = true;

            adminOfficerOption.disabled = false;
            adminOfficerOption.classList.remove('disabled-option');
            adminOfficerOption.style.opacity = '1';
        } else {
        
            roleDropdown.disabled = false;
            roleDropdown.value = '';

            adminOfficerOption.disabled = true;
            adminOfficerOption.classList.add('disabled-option');
            adminOfficerOption.style.opacity = '0.5';
        }
    }

});
