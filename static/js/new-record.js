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

// Handle QR code printing and saving
document.addEventListener('DOMContentLoaded', function () {
    const printQRButton = document.getElementById('printQR');
    const saveQRButton = document.getElementById('saveQR');
    const qrCodeImage = document.getElementById('qrCodeImage');

    // Handle printing the QR code
    if (printQRButton) {
        printQRButton.addEventListener('click', function () {
            const printWindow = window.open('', '', 'height=600,width=800');
            printWindow.document.write('<html><head><title>Print QR Code</title>');
            printWindow.document.write('<style>');
            printWindow.document.write('body { font-family: Inter, sans-serif; text-align: center; width: 55mm; margin: 0 auto; }');
            printWindow.document.write('img { max-width: 45mm; height: auto; display: block; margin: 0 auto; }'); // Limit QR code width to 45mm
            printWindow.document.write('p { font-size: 14px; font-weight: bold; margin: 5px 0; padding: 0; }'); // Adjust font size
            printWindow.document.write('</style>');
            printWindow.document.write('</head><body>');
            printWindow.document.write('<p>{{ str_routes }}</p>');
            printWindow.document.write('<img src="' + qrCodeImage.src + '" />');
            printWindow.document.write('<p>{{ str_tracking_no }}</p>');
            printWindow.document.close();
            printWindow.focus();
            printWindow.print();
        });
    }

    // Handle saving the QR code
    if (saveQRButton) {
        saveQRButton.addEventListener('click', function () {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const strRoutes = "{{ str_routes|escapejs }}";
            const strTrackingNo = "{{ str_tracking_no|escapejs }}";
            const documentNo = "{{ document_no }}";
            const qrCodeImg = new Image();
            qrCodeImg.src = qrCodeImage.src;

            qrCodeImg.onload = function () {
                canvas.width = qrCodeImg.width;
                canvas.height = qrCodeImg.height + 60; // Extra space for text
                // Fill the canvas with a white background
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                // Draw the QR code image
                ctx.drawImage(qrCodeImg, 0, 30); // Adjust y position for QR code
                // Set font for the text
                ctx.font = 'bold 31px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillStyle = 'black'; // Set text color to black
                // Add text above and below the QR code
                ctx.fillText(strRoutes, canvas.width / 2, 43);
                ctx.font = 'bold 20px Inter, sans-serif';
                ctx.fillText(strTrackingNo, canvas.width / 2, canvas.height - 24);
                // Trigger download
                const link = document.createElement('a');
                link.href = canvas.toDataURL('image/png');
                link.download = 'doc_' + documentNo + '_qr_code.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };
        });
    }
});
