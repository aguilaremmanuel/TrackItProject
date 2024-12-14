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
            bindApproveButtons();
            bindRejectButtons();
    });
}

function bindApproveButtons() {
    
    const table = document.querySelector('#recordsTable');
    const approveButtons = document.querySelectorAll('.approve-btn');
    const approveModal = new bootstrap.Modal(document.getElementById('approveDocumentModal'),{
        backdrop: 'static',
        keyboard: false
    });
    const approveMultipleDocumentsModal = new bootstrap.Modal(document.getElementById('approveMultipleDocumentsModal'),{
        backdrop: 'static',
        keyboard: false
    });
    
    approveButtons.forEach(button => {

        button.addEventListener('click', function () {

            const documentNo = this.getAttribute('data-document-no');
            const confirmUrgentDocModalForMultipleUpdate = new bootstrap.Modal(document.getElementById('confirmUrgentDocModalForMultipleUpdate'),{
                backdrop: 'static',
                keyboard: false
            });

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
                approveMultipleDocumentsModal.show();

                let remarksNo;
                let activityLogsNo = [];

                document.getElementById('confirmMultipleDocsApprove').addEventListener('click', function() {
                    
                    checkedValues.forEach((element, index) => {
                        
                        fetch(`/document-update-status/approve/${element}`)
                            .then(response => response.json())
                            .then(data => {
                                if(index == 0) {
                                    remarksNo = data.remarks_no;
                                }
                                activityLogsNo.push(data.activity_log_no);
                            })
                            .catch(error => console.error('Error', error));
                    });

                    approveMultipleDocumentsModal.hide();

                });

                const saveRemarksBtn =  document.getElementById('saveRemarksMultiple');
                saveRemarksBtn.addEventListener('click', function (e) {

                    e.preventDefault();

                    const form = document.getElementById('remarksFormForMultipleUpdate');
                    const formData = new FormData(form);

                    formData.append('activityLogsNo', JSON.stringify(activityLogsNo)); 
                    formData.append('checkedValues', JSON.stringify(checkedValues));

                    fetch(`/multiple-update-remarks/${remarksNo}/`, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': getCSRFToken(),  // Include the CSRF token in the request header
                        }
                    })
                    .then(response => response.json())
                    .then(data => {

                        if(data.high_priority_detected) {
                            document.getElementById('remarksDisplayForMultipleUpdate').innerHTML = data.highlighted_remarks;

                            confirmUrgentDocModalForMultipleUpdate.show();

                            document.getElementById('cancelChangePrioLevelBtnForMultipleUpdate').addEventListener('click', function() {
                                confirmUrgentDocModalForMultipleUpdate.hide();
                            });

                            document.getElementById('confirmChangePrioLevelBtnForMultipleUpdate').addEventListener('click', function() {

                                confirmUrgentDocModalForMultipleUpdate.hide();

                                const remarks = document.getElementById('remarksMultiple').value;
                                const fileInput = document.getElementById('attachmentFileMultiple');

                                const formData = new FormData();
                                formData.append('remarks_no', remarksNo);
                                formData.append('activity_logs_no', JSON.stringify(activityLogsNo));
                                formData.append('checked_values', JSON.stringify(checkedValues));
                                formData.append('remarks', remarks);

                                if (fileInput.files.length > 0) {
                                    formData.append('attachment', fileInput.files[0]);
                                }

                                fetch(`/change-priority-level-multiple-documents/`, {
                                    method: 'POST',
                                    headers: {
                                        'X-CSRFToken': getCSRFToken(),  
                                    },
                                    body: formData, 
                                })
                                .then(response => response.json())
                                .then(data => {
                                    console.log("success");
                                })
                                .catch(error => console.error('Error', error));


                            });

                        } else {
                            console.log("wala nadetect");
                        }

                    })
                    .catch(error => console.error('Error', error));

                });

            } else {
                approveModal.show();

                document.getElementById('confirmApprove').addEventListener('click', function() {

                    fetch(`/document-update-status/approve/${checkedValues[0]}/`)
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

        })

    });

    document.getElementById('cancelApproveBtn').addEventListener('click', function() {
        approveModal.hide();
        resetSelection(table);
    });

    document.getElementById('cancelApproveMultipleDocsBtn').addEventListener('click', function() {
        approveMultipleDocumentsModal.hide();
        resetSelection(table);
    });

    document.getElementById('confirmApprove').addEventListener('click', function () {
        approveModal.hide();
        actionMessage.textContent = "The document has been successfully approved. Add any additional remarks and upload necessary attachment related to this action below, or leave as blank if not applicable.";
        //remarksModal.show();
    });

}

function bindRejectButtons() {

    const table = document.querySelector('#recordsTable');
    const rejectButtons = document.querySelectorAll('.reject-btn');
    const rejectModal = new bootstrap.Modal(document.getElementById('rejectDocumentModal'),{
        backdrop: 'static',
        keyboard: false
    });
    const rejectMultipleDocumentsModal = new bootstrap.Modal(document.getElementById('rejectMultipleDocumentsModal'),{
        backdrop: 'static',
        keyboard: false
    });

    rejectButtons.forEach(button => {

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

                document.getElementById('selectedRejectDocsCount').innerHTML = checkedValues.length;
                rejectMultipleDocumentsModal.show();

                let remarksNo;
                let activityLogsNo = [];

                document.getElementById('confirmMultipleDocsReject').addEventListener('click', function() {
                    
                    checkedValues.forEach((element, index) => {
                        
                        fetch(`/document-update-status/reject/${element}`)
                            .then(response => response.json())
                            .then(data => {
                                if(index == 0) {
                                    remarksNo = data.remarks_no;
                                }
                                activityLogsNo.push(data.activity_log_no);
                            })
                            .catch(error => console.error('Error', error));
                    });

                    rejectMultipleDocumentsModal.hide();

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
                        console.log("successfully rejected multiple documents");
                    })
                    .catch(error => console.error('Error', error));

                });


            } else {

                rejectModal.show();

                document.getElementById('confirmReject').addEventListener('click', function() {

                    fetch(`/document-update-status/reject/${checkedValues[0]}/`)
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

        })

    });

    document.getElementById('rejectModalCloseBtn').addEventListener('click', function() {
        rejectModal.hide();
        resetSelection(table);
    });

    document.getElementById('rejectMultipleDocumentsModalCloseBtn').addEventListener('click', function() {
        rejectMultipleDocumentsModal.hide();
        resetSelection(table);
    });

    document.getElementById('confirmReject').addEventListener('click', function () {
        rejectModal.hide();
        actionMessage.textContent = "The document has been rejected. Add any additional remarks and upload necessary attachment related to this action below, or leave as blank if not applicable.";
    });

}

function resetSelection(table) {

    const checkboxes = table.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    const selectAllBtn = document.getElementById('selectAllBtn');
    // selectAllBtn.innerHTML = 'Select All';
    selectAllBtn.innerHTML = "<i class='bx bxs-checkbox-checked fs-4' style='color:#2e72ea' ></i>";

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