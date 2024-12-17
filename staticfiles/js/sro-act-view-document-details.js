
document.addEventListener('DOMContentLoaded', function() {
    
    const userID = document.querySelector('.user-id').getAttribute('data-user-id');
    const role = userID.split('-')[0];
    const viewButtons = document.querySelectorAll('.viewDocumentBtn');

    viewButtons.forEach(button => {
        button.addEventListener('click', (event) => {

            const documentNo = button.getAttribute('data-document-no');

            document.getElementById('loadingSpinner').style.display = 'block';
            document.getElementById('documentDetailsContent').style.display = 'none';
            document.getElementById('activitiesContent').style.display = 'none';
            document.getElementById('activitiesTableBody').innerHTML = ''; 

            fetch(`/fetch-document-details/${documentNo}/`)
                .then(response => response.json())
                .then(data => {
                    
                    document.getElementById('documentTrackingNumber').textContent = data.tracking_no;
                    document.getElementById('documentSender').textContent = data.sender_name;
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

                    let nextActivityToDisplayLast = null;

                    let start = false;

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
                        
                        if(role=='SRO') {
                            if(activity.user_id === userID && activity.activity === 'Document Resolved') {
                                start = true;
                            }
                        } else {
                            if(activity.user_id === userID && activity.activity === 'Document Endorsed by Action Officer') {
                                start = true;
                            }
                        }
                        

                        if(start){
                            activitiesTableBody.appendChild(row);
                        }

                        //bindViewAttachmentButton();
                    });

                    document.getElementById('documentTitleLink').setAttribute('data-document-no', documentNo);
                    
                    // Hide spinner and show content once data is loaded
                    document.getElementById('loadingSpinner').style.display = 'none';
                    document.getElementById('documentDetailsContent').style.display = 'flex';
                    document.getElementById('activitiesContent').style.display = 'flex';

                })
                .catch(error => {
                    console.error('Error:', error);
                });

        });
    });

});