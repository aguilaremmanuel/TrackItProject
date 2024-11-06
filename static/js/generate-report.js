function setEndDates() {
    let today = new Date().toISOString().split('T')[0];
    let dateInputs = document.querySelectorAll('input[type="date"]');
    // Set the max attribute for all date inputs
    dateInputs.forEach(function(input) {
        input.setAttribute('max', today);
    });
}

function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById('EmployeeOfficeCategory').addEventListener('change', function () {

    var selectedEmployeeOffice = this.value;
    var targetEmployeeSelect = document.getElementById('TargetEmployee');

    if (selectedEmployeeOffice) {
        fetch(`/load-target-employees/?selected_employee_office=${selectedEmployeeOffice}`)
        .then(response => response.json())
        .then(data => {
            // Clear previous options
            targetEmployeeSelect.innerHTML = '<option value="" selected disabled hidden>Select Target Employee</option>';
            // Enable the dropdown
            targetEmployeeSelect.disabled = false;
            // Populate new options
            data.forEach(function (item) {

                display_option = "(" + item.employee_id + ") - " + item.lastname + ", " + item.firstname

                var option = new Option(display_option, item.employee_id);
                targetEmployeeSelect.add(option);
            });
        });
    } else {
        targetEmployeeSelect.innerHTML = '<option value="">Select Document Type</option>';
        targetEmployeeSelect.disabled = true;
    }
});

document.addEventListener('DOMContentLoaded', function () {

    setEndDates();

    const employeeReportForm = document.getElementById('employeeReportForm');
    const generateEmployeeReportBtn = document.getElementById('generateEmployeeReportBtn');
    const employeeReportModal = new bootstrap.Modal(document.getElementById('employeeReportModal'));
    const confirmEmployeeReportCreation = new bootstrap.Modal(document.getElementById('confirmEmployeeReportCreation'));

    generateEmployeeReportBtn.addEventListener('click', function(event) {
        event.preventDefault();
        if (employeeReportForm.checkValidity()) {
            employeeReportModal.hide()
            confirmEmployeeReportCreation.show();
        } else {
            employeeReportForm.reportValidity();
        }
    });

    const cancelCreateEmployeeReport = document.getElementById('cancelCreateEmployeeReport');
    cancelCreateEmployeeReport.addEventListener('click', function() {
        employeeReportModal.show();
    });

    const officeReportForm = document.getElementById('officeReportForm');
    const generateOfficeReportBtn = document.getElementById('generateOfficeReportBtn');
    const officeReportModal = new bootstrap.Modal(document.getElementById('officeReportModal'));
    const confirmOfficeReportCreation = new bootstrap.Modal(document.getElementById('confirmOfficeReportCreation'));

    generateOfficeReportBtn.addEventListener('click', function(event) {
        event.preventDefault();
        if (officeReportForm.checkValidity()) {
            officeReportModal.hide()
            confirmOfficeReportCreation.show();
        } else {
            officeReportForm.reportValidity();
        }
    });

    const cancelCreateOfficeReport = document.getElementById('cancelCreateOfficeReport');
    cancelCreateOfficeReport.addEventListener('click', function() {
        officeReportModal.show();
    });


    const confirmEmployeeReportCreateBtn = document.getElementById('confirmEmployeeReportCreate');

    confirmEmployeeReportCreateBtn.addEventListener('click', function() {

        confirmEmployeeReportCreation.hide()

        const formData = new FormData(employeeReportForm);

        fetch('/new-employee-report/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),  // Include the CSRF token in the request header
            }
        })
        .then(response => response.json())
        .then(data => {

            if (!data.validDates) {
                const invalidDatesModal = new bootstrap.Modal(document.getElementById('invalidDatesModal'));
                invalidDatesModal.show();
            } else {
                employeeReportForm.reset();
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });

    });

    const confirmOfficeReportCreateBtn = document.getElementById('confirmOfficeReportCreateBtn');

    confirmOfficeReportCreateBtn.addEventListener('click', function() {

        confirmOfficeReportCreation.hide()

        const formData = new FormData(officeReportForm);

        fetch('/new-office-report/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),  // Include the CSRF token in the request header
            }
        })
        .then(response => response.json())
        .then(data => {
            if (!data.validDates) {
                const invalidDatesModal = new bootstrap.Modal(document.getElementById('invalidDatesModal'));
                invalidDatesModal.show();
            }else {
                officeReportForm.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    const deleteReportModal = document.getElementById('deleteReportModal');
    deleteReportModal.addEventListener('show.bs.modal', function(event) {

        const button = event.relatedTarget;
        const reportNo = button.getAttribute('data-report-no');

        const confirmDeleteBtn = document.getElementById('confirmDelete');
        confirmDeleteBtn.onclick = function() {
            
            const modalInstance = bootstrap.Modal.getInstance(deleteReportModal);
            modalInstance.hide(); 

            fetch(`/delete-report/${reportNo}/`)
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                })
                .catch(error => console.error('Error', error));
        };

    });

});





