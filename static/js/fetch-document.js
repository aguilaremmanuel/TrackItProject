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

             // Show spinner and hide content before fetching data
             document.getElementById('loadingSpinner').style.display = 'block';
             document.getElementById('documentDetailsContent').style.display = 'none';
             document.getElementById('activitiesContent').style.display = 'none';
             document.getElementById('activitiesTableBody').innerHTML = ''; // Clear previous entries

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
                    
                    const activitiesTableBody = document.getElementById('activitiesTableBody');
                    activitiesTableBody.innerHTML = ''; // Clear previous entries

                    data.activity_logs.forEach(activity => {
                        const row = document.createElement('tr');
                        
                        row.innerHTML = `
                            <td style="white-space: nowrap;">${activity.date}<br>${activity.time}</td>
                            <td style="white-space: nowrap;">${activity.user_id}</td>
                            <td>${activity.name}</td>
                            <td>${activity.office}</td>
                            <td style="white-space: nowrap;">${activity.role}</td>
                            <td><i>${activity.remarks}</i></td>
                            <td style="white-space: nowrap;"><a href="#" data-bs-toggle="modal" data-bs-target="#viewAttachmentModal" id="viewAttachmentLink">View Attachment</a></td>
                            <td>${activity.activity}</td>
                        `;

                        activitiesTableBody.appendChild(row);
                    });
                    
                    document.getElementById('documentTitleLink').setAttribute('data-document-no', documentNo);
                    document.getElementById('generateDocumentReportBtn').setAttribute('data-document-no', documentNo);

                    // Hide spinner and show content once data is loaded
                    document.getElementById('loadingSpinner').style.display = 'none';
                    document.getElementById('documentDetailsContent').style.display = 'flex';
                    document.getElementById('activitiesContent').style.display = 'flex';
                   
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

document.addEventListener('DOMContentLoaded', function() {
    fetchDocuments();
    scanningQRCode();
    setInterval(fetchDocuments, 3000);
});