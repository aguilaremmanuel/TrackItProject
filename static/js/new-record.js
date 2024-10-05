// On page load, read the URL parameter and update the class
document.addEventListener('DOMContentLoaded', function () {
    const params = new URLSearchParams(window.location.search);
    const status = params.get('status');
    if (status) {
        // Assuming you want to add the class to the element with ID 'targetElement'
        document.querySelector('#new').classList.add(status);
    }
    /*
    try {
        const generateQRCodeModal = new bootstrap.Modal(document.getElementById('generateQRCode'));
        // Automatically show the generateQRCode modal when the page loads
        if (generateQRCodeModal) {
            generateQRCodeModal.show();
        }
    } catch (error) {
        console.error("QR Code modal could not be shown:", error);
    }
    */
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

document.addEventListener("DOMContentLoaded", function() {

    const confirmCreateBtn =  document.getElementById('confirmCreate');
    const form = document.getElementById('recordForm');
    const generateQRCodeModal = new bootstrap.Modal(document.getElementById('generateQRCode'));

    // Handle record form submission on confirm
    confirmCreateBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch('/add-record/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),  // Include the CSRF token in the request header
            }
        })
        .then(response => response.json())
        .then(data => {

            if(data.recordExists) {
                document.getElementById('existingTrackingNo').textContent = data.trackingNo;
                const recordExistsModal = new bootstrap.Modal(document.getElementById('recordExistsModal'));
                recordExistsModal.show();
            } else {
                document.getElementById('routesQr').textContent = data.str_routes;
                document.getElementById('qrCodeImage').src = data.qr_code_url;
                document.getElementById('trackingNoQr').textContent = data.str_tracking_no;
                document.getElementById('str_routesQr').textContent = data.str_routes_titles;
                generateQRCodeModal.show();
                form.reset();
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });
    }); 
});

document.addEventListener('DOMContentLoaded', function () {
    const printQRButton = document.getElementById('printQR');
    const saveQRButton = document.getElementById('saveQR');
    if (printQRButton) {
        printQRButton.addEventListener('click', function () {
            const routes = document.getElementById('routesQr').textContent;
            const trackingNo = document.getElementById('trackingNoQr').textContent;
            const qrCodeImage = document.getElementById('qrCodeImage');
            const printWindow = window.open('', '', 'height=600,width=700');
            const routesTitles = document.getElementById('str_routesQr').textContent;
            printWindow.document.write('<html><head><title>Print QR Code</title>');
            printWindow.document.write('<style>');
            printWindow.document.write('body, html { font-family: Inter, sans-serif; text-align: center; margin: 0; padding: 0; }');
            printWindow.document.write('img { max-width: 45mm;}'); // Limit QR code width to 45mm
            printWindow.document.write('p { font-size: 18px; font-weight: bold; margin: 0; padding: 0; }'); // Adjust font size
            printWindow.document.write('@media print { body, html { margin: 0; padding: 0; } }'); // Additional print-specific styles
            printWindow.document.write('</style>');
            printWindow.document.write('</head><body>');;    
            printWindow.document.write('<div style="width: 165px; display: flex; flex-direction: column; align-items: center;">'); // Centering div
            printWindow.document.write('<p>' + routes + '</p>');
            printWindow.document.write('<p style="font-size: 9px; font-weight: 400">('+ routesTitles +')</p>');
            printWindow.document.write('<img src="' + qrCodeImage.src + '" />');
            printWindow.document.write('<p style="font-size: 13px;">' + trackingNo + '</p>');
            printWindow.document.write('<p style="font-size: 8px; font-weight: 400">(Document Tracking Number)</p>');
            printWindow.document.write('</div>');
            printWindow.document.write('</body></html>');
            printWindow.document.close();
            printWindow.focus();
            printWindow.print();
    });
    }
    if (saveQRButton) {
        saveQRButton.addEventListener('click', function () {

            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const routes = document.getElementById('routesQr').textContent;
            const routesTitles = "(" + document.getElementById('str_routesQr').textContent + ")";
            const trackingNo = document.getElementById('trackingNoQr').textContent;

            const qrCodeImage = document.getElementById('qrCodeImage');
            const qrCodeImg = new Image();
            qrCodeImg.src = qrCodeImage.src;

            qrCodeImg.onload = function () {
                canvas.width = qrCodeImg.width;
                canvas.height = qrCodeImg.height + 110; // Extra space for text
                // Fill the canvas with a white background
                ctx.fillStyle = 'white';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                // Draw the QR code image
                ctx.drawImage(qrCodeImg, 0, 50); // Adjust y position for QR code
                // Set font for the text
                ctx.font = 'bold 31px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillStyle = 'black'; 
                ctx.fillText(routes, canvas.width / 2, 43);
                ctx.font = '16px Inter, sans-serif';
                ctx.fillText(routesTitles, canvas.width / 2, 65);
                ctx.font = 'bold 20px Inter, sans-serif';
                ctx.fillText(trackingNo, canvas.width / 2, canvas.height - 54);
                ctx.font = '16px Inter, sans-serif';
                ctx.fillText("(Document Tracking Number)", canvas.width / 2, canvas.height - 35);
                // Trigger download
                const link = document.createElement('a');
                link.href = canvas.toDataURL('image/png');
                link.download = 'qr_code.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };

        });
    }
});

