function fetchDocuments() {

    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = document.getElementById('searchInput');
    let searchValue = searchQuery.value.trim()
    let updateUrl = searchQuery.getAttribute('data-url');
    let fetchUrl = updateUrl + `?search=${encodeURIComponent(searchValue)}`;
    
    if (!searchValue) {
        const sortBy = urlParams.get('sort_by') || '';
        const order = urlParams.get('order') || 'asc';
        fetchUrl = updateUrl + "?sort_by=" + sortBy + "&order=" + order;
    }

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            
            document.getElementById('docTableBody').innerHTML = data.html;
            let noOfRecords = document.getElementById('docuLength').value;
            document.getElementById('recordCount').textContent = noOfRecords;
            bindViewButtons();
    });
}

function bindViewButtons() {
    const viewButtons = document.querySelectorAll('.viewDocumentBtn');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function () {
            const documentNo = this.getAttribute('data-document-no');

             document.getElementById('loadingSpinner').style.display = 'block';
             document.getElementById('documentDetailsContent').style.display = 'none';
             document.getElementById('activitiesContent').style.display = 'none';
             document.getElementById('activitiesTableBody').innerHTML = ''; 

            // Fetch document details via AJAX
            fetch(`/fetch-document-details/${documentNo}/`)
                .then(response => response.json())
                .then(data => {

                    // Populate the modal with the new data
                    document.getElementById('documentTrackingNumber').textContent = data.tracking_no;
                    document.getElementById('documentSender').textContent = data.sender_name;
                    document.getElementById('documentStatus').textContent = data.status;
                    document.getElementById('documentType').textContent = data.document_type.charAt(0).toUpperCase() + data.document_type.slice(1)
                    document.getElementById('documentPriority').textContent = data.priority;
                    document.getElementById('documentSubject').textContent = data.subject;

                    if (data.routes_txt) {
                        document.getElementById('documentRoutesTxt').classList.remove('d-none');
                        document.getElementById('documentRoutes').textContent = data.routes_txt;
                    } else {
                        document.getElementById('documentRoutesTxt').classList.add('d-none');
                    }

                    const activitiesTableBody = document.getElementById('activitiesTableBody');
                    activitiesTableBody.innerHTML = ''; // Clear previous entries

                    data.activity_logs.forEach(activity => {
                        const row = document.createElement('tr');
                        
                        row.innerHTML = `
                            <td style="white-space: nowrap;">${activity.date}<br>${activity.time}</td>
                            <td style="white-space: nowrap;">${activity.employee_id}</td>
                            <td>${activity.name}</td>
                            <td>${activity.office}</td>
                            <td style="white-space: nowrap;">${activity.role}</td>
                        `;

                        if(activity.remarks) {
                            row.innerHTML += `<td><i>${activity.remarks}</i></td>`;
                        } else {
                            row.innerHTML += '<td style="opacity: 40%;">-no remarks-</td>';
                        }

                        if (activity.file_attachment) {
                            const fileName = activity.file_attachment.split('/').pop();
                            row.innerHTML += `<td style="white-space: nowrap;"><button class="view-attachment-btn" id="viewAttachmentLink" data-filepath="${activity.file_attachment}" data-bs-toggle="modal" data-bs-target="#viewAttachmentModal">${fileName}</button></td>`;
                        } else {
                            // Add an empty <td> if no file_attachment to maintain table structure
                            row.innerHTML += `<td style="opacity: 40%;">-no attachment-</td>`;
                        }
                        row.innerHTML += `<td>${activity.activity} <br> <span style='font-size: 12px; opacity: 50%;'>Sent to: ${activity.receiver_name} </span> </td>`;
                        activitiesTableBody.appendChild(row);

                        bindViewAttachmentButton();
                    });

                    document.getElementById('documentTitleLink').setAttribute('data-document-no', documentNo);
                    
                    // Hide spinner and show content once data is loaded
                    document.getElementById('loadingSpinner').style.display = 'none';
                    document.getElementById('documentDetailsContent').style.display = 'flex';
                    document.getElementById('activitiesContent').style.display = 'flex';

                    document.getElementById('generateDocumentReportBtn').setAttribute('data-document-no', documentNo);
                   
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('loadingSpinner').style.display = 'none';
                });
                
        });
    });
}

function scanningQRCode() {
    var inputField = document.getElementById('scannedQrURL');
    var scanQRCodeModal = document.getElementById('scanQRCodeModal');
        scanQRCodeModal.addEventListener('shown.bs.modal', function () {
            // Focus on the input field
            inputField.value = "";
            document.getElementById('scannedQrURL').focus();
        });
    var typingTimer; // Timer identifier
    var doneTypingInterval = 1000; // Time in ms (1 second)
    
    inputField.addEventListener('input', function() {

        clearTimeout(typingTimer); // Clear the timer on every input
        // Set a new timer
        typingTimer = setTimeout(function() {
            var inputValue = inputField.value.trim(); // Trim whitespace

            window.location.href = inputValue; // Redirect to the input URL
            // Hide the modal after processing the input
            var bootstrapModalInstance = bootstrap.Modal.getInstance(scanQRCodeModal);
            bootstrapModalInstance.hide();
        }, doneTypingInterval); 
    });
}

function bindViewAttachmentButton() {
    const viewAttachmentButtons = document.querySelectorAll('.view-attachment-btn');

    if(viewAttachmentButtons) {
        viewAttachmentButtons.forEach(button => {
            button.addEventListener('click', function () {
                const rawfilepath = this.getAttribute('data-filepath')
                const filepath = rawfilepath + "?v=" + new Date().getTime();
                const fileURL = `${window.location.origin}${filepath}`; 
                // Set iframe source to display the PDF
                document.getElementById('pdfFrame').src = fileURL;
                // Update the attachment name in the modal
                const fileName = rawfilepath.split('/').pop();
                document.getElementById('attachmentName').textContent = fileName;
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    fetchDocuments();
    scanningQRCode();
    setInterval(fetchDocuments, 3000);

});