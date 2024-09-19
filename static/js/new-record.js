document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('status');
    if (status) {
        document.querySelector('#new').classList.add(status);
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
    const modal = new bootstrap.Modal(document.getElementById('confirmRecordCreation'));

    // Add an event listener to the submit button
    submitBtn.addEventListener('click', function (event) {
        // Prevent default form submission
        event.preventDefault();

        // Check if the form is valid
        if (form.checkValidity()) {
            // If the form is valid, show the confirmation modal
            modal.show();
        } else {
            // If the form is invalid, trigger validation messages
            form.reportValidity();
        }
    });
});

document.getElementById('DocumentCategory').addEventListener('change', function() {
    var category = this.value;
    var docTypeSelect = document.getElementById('DocumentType');

    if (category) {
        fetch(`/load-document-types/?category=${category}`)
        .then(response => response.json())
        .then(data => {
            // Clear previous options
            docTypeSelect.innerHTML = '<option value="">Select Document Type</option>';
            // Enable the dropdown
            docTypeSelect.disabled = false;
            // Populate new options
            data.forEach(function(item) {
                var option = new Option(item.document_type, item.document_no);
                docTypeSelect.add(option);
            });
        });
    } else {
        docTypeSelect.innerHTML = '<option value="">Select Document Type</option>';
        docTypeSelect.disabled = true;
    }
});

document.getElementById('confirmCreate').addEventListener('click', function() {
    document.getElementById('recordForm').submit();
});





