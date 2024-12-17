function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

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
            bindRouteButtons();
            bindArchiveButtons();
    });
}

function bindRouteButtons() {
    
    const table = document.querySelector('#recordsTable');
    const routeButtons = document.querySelectorAll('.route-btn');
    const routeModal = new bootstrap.Modal(document.getElementById('routeDocumentModal'),{
        backdrop: 'static',
        keyboard: false
    });
    const routeMultipleDocumentsModal = new bootstrap.Modal(document.getElementById('routeMultipleDocumentsModal'),{
        backdrop: 'static',
        keyboard: false
    });
    
    routeButtons.forEach(button => {

        button.addEventListener('click', function () {

            const documentNo = this.getAttribute('data-document-no');

            const checkbox = document.querySelector(`input[type="checkbox"][value="${documentNo}"]`);

            if (checkbox && checkbox.checked) {
                console.log("this option is checked");
            } else {
                checkbox.checked = true; 
                const event = new Event('change', { bubbles: true, cancelable: true });
                checkbox.dispatchEvent(event);
            }

            const checkboxes = table.querySelectorAll('input[type="checkbox"]');
            const checkedValues = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);
        
            if (checkedValues.length > 1) {

                document.getElementById('selectedDocsCount').innerHTML = checkedValues.length;
                routeMultipleDocumentsModal.show();

                let remarksNo;
                let activityLogsNo = [];

                document.getElementById('confirmMultipleDocsRoute').addEventListener('click', function() {
                    
                    checkedValues.forEach((element, index) => {
                        
                        fetch(`/document-update-status/route/${element}`)
                            .then(response => response.json())
                            .then(data => {
                                if(index == 0) {
                                    remarksNo = data.remarks_no;
                                }
                                activityLogsNo.push(data.activity_log_no);
                            })
                            .catch(error => console.error('Error', error));
                    });

                    routeMultipleDocumentsModal.hide();

                });
                
                const saveRemarksBtn =  document.getElementById('saveRemarksMultiple');
                saveRemarksBtn.addEventListener('click', function (e) {

                    e.preventDefault();

                    const form = document.getElementById('remarksFormForMultipleUpdate');
                    const formData = new FormData(form);

                    formData.append('activityLogsNo', JSON.stringify(activityLogsNo)); 
                    formData.append('checkedValues', JSON.stringify(checkedValues));

                    fetch(`/multiple-update-reject-remarks/${remarksNo}/`, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken(),
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log("SUCCESS");
                    })
                    .catch(error => console.error('Error', error));
                
                });
                
            } else {
                
                routeModal.show();
                
                document.getElementById('confirmRoute').addEventListener('click', function() {

                    fetch(`/document-update-status/route/${checkedValues[0]}/`)
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('saveRemarks').setAttribute('data-remarks-no', data.remarks_no);
                            document.getElementById('saveRemarks').setAttribute('data-document-no', documentNo);
                            document.getElementById('saveRemarks').removeAttribute('data-activity-log-no');
                            document.getElementById('saveRemarks').setAttribute('data-activity-log-no', data.activity_log_no);
                        })
                        .catch(error => console.error('Error', error));

                });
                
            }
            
        });

    });

    
    document.getElementById('cancelRouteBtn').addEventListener('click', function() {
        routeModal.hide();
        resetSelection(table);
    });
    
    document.getElementById('cancelRouteMultipleDocsBtn').addEventListener('click', function() {
        routeMultipleDocumentsModal.hide();
        resetSelection(table);
    });

    document.getElementById('confirmRoute').addEventListener('click', function () {
        routeModal.hide();
    });
    
}

function bindArchiveButtons() {
    
    const table = document.querySelector('#recordsTable');
    const archiveButtons = document.querySelectorAll('.archive-btn');
    const archiveModal = new bootstrap.Modal(document.getElementById('archiveDocumentModal'),{
        backdrop: 'static',
        keyboard: false
    });
    const archiveMultipleDocumentsModal = new bootstrap.Modal(document.getElementById('archiveMultipleDocumentsModal'),{
        backdrop: 'static',
        keyboard: false
    });
    
    archiveButtons.forEach(button => {

        button.addEventListener('click', function () {

            const documentNo = this.getAttribute('data-document-no');

            const checkbox = document.querySelector(`input[type="checkbox"][value="${documentNo}"]`);

            if (checkbox && checkbox.checked) {
                console.log("this option is checked");
            } else {
                checkbox.checked = true; 
                const event = new Event('change', { bubbles: true, cancelable: true });
                checkbox.dispatchEvent(event);
            }

            const checkboxes = table.querySelectorAll('input[type="checkbox"]');
            const checkedValues = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);
        
            if (checkedValues.length > 1) {

                console.log("checked vaues: " + checkedValues.length);

                document.getElementById('selectedDocsCountArchive').innerHTML = checkedValues.length;
                archiveMultipleDocumentsModal.show();

                let remarksNo;
                let activityLogsNo = [];

                document.getElementById('confirmMultipleDocsArchive').addEventListener('click', function() {
                    
                    checkedValues.forEach((element, index) => {
                        
                        fetch(`/document-update-status/archive/${element}`)
                            .then(response => response.json())
                            .then(data => {
                                if(index == 0) {
                                    remarksNo = data.remarks_no;
                                }
                                activityLogsNo.push(data.activity_log_no);
                            })
                            .catch(error => console.error('Error', error));
                    });

                    archiveMultipleDocumentsModal.hide();

                });
                
            } else {
                
                archiveModal.show();
                
                document.getElementById('confirmArchive').addEventListener('click', function() {

                    fetch(`/document-update-status/archive/${checkedValues[0]}/`)
                        .then(response => response.json())
                        .then(data => {
                            console.log("successfully archived");
                        })
                        .catch(error => console.error('Error', error));

                });
                
            }
            
        });

    });

    
    document.getElementById('cancelArchiveBtn').addEventListener('click', function() {
        archiveModal.hide();
        resetSelection(table);
    });
    
    document.getElementById('cancelArchiveMultipleDocsBtn').addEventListener('click', function() {
        archiveMultipleDocumentsModal.hide();
        resetSelection(table);
    });

    document.getElementById('confirmArchive').addEventListener('click', function () {
        archiveModal.hide();
    });
    
}

function resetSelection(table) {

    const checkboxes = table.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    

    const selectAllBtn = document.getElementById('selectAllBtn');
    selectAllBtn.innerHTML = "<i class='bx bxs-checkbox-checked fs-4' style='color:#2e72ea' ></i>";
    //selectAllBtn.innerHTML = 'Select All';

    documents_no = [0,0]

    fetch(`/select-all-documents/deselect-all/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() 
        },
        body: JSON.stringify({ documents_no }) 
    })
        .then(response => response.json())
        .then(data => {
            console.log("Success");
        })
        .catch(error => {
            console.error('Error:', error);
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