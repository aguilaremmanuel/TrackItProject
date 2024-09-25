// On page load, read the URL parameter and update the class
document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('status');
    if (status) {
        // Assuming you want to add the class to the element with ID 'targetElement'
        document.querySelector('#new').classList.add(status);
    }

    try {
        const generateQRCodeModal = new bootstrap.Modal(document.getElementById('generateQRCode'));
        // Automatically show the generateQRCode modal when the page loads
        if (generateQRCodeModal) {
            generateQRCodeModal.show();
        }
    } catch (error) {
        console.error("QR Code modal could not be shown:", error);
    }

});

// Add an event listener to the submit button
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
    const modal = new bootstrap.Modal(document.getElementById('confirmRecordCreation'));

    submitBtn.addEventListener('click', function (event) {
        event.preventDefault();
        if (form.checkValidity()) {
            modal.show();
        } else {
            form.reportValidity();
        }
    });
});

// Handle dynamic DocumentType dropdown population
document.getElementById('DocumentCategory').addEventListener('change', function () {
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
            data.forEach(function (item) {
                var option = new Option(item.document_type, item.document_no);
                docTypeSelect.add(option);
            });
        });
    } else {
        docTypeSelect.innerHTML = '<option value="">Select Document Type</option>';
        docTypeSelect.disabled = true;
    }
});

// Handle record form submission on confirm
document.getElementById('confirmCreate').addEventListener('click', function () {
    document.getElementById('recordForm').submit();
}); 