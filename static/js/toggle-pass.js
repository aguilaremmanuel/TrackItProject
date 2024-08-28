document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#password2');

    const departmentSelect = document.querySelector('#selectDept');
    const roleSelect = document.querySelector('#selectRole');

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

    departmentSelect.addEventListener('change', function () {
        const selectedDepartment = departmentSelect.value;

        if (selectedDepartment === 'ADM') {
            roleSelect.value = 'ADO';
            roleSelect.setAttribute('disabled', 'disabled');
        } else {
            roleSelect.removeAttribute('disabled');
            const restrictedRoles = ['ADO'];  // Restricted roles for certain departments
            if (['ACC', 'BMD', 'CSR', 'PRL'].includes(selectedDepartment)) {
                restrictedRoles.forEach(role => {
                    const option = roleSelect.querySelector(`option[value="${role}"]`);
                    if (option) {
                        option.setAttribute('disabled', 'disabled');
                    }
                });
            } else {
                restrictedRoles.forEach(role => {
                    const option = roleSelect.querySelector(`option[value="${role}"]`);
                    if (option) {
                        option.removeAttribute('disabled');
                    }
                });
            }
        }
    });
});
