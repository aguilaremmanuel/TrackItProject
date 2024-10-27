document.getElementById('trackDocument').addEventListener('click', function() {
            
    const documentNo = document.getElementById('trackDocument').getAttribute('data-document-no');
        // Fetch document details via AJAX
    fetch(`/fetch-document-details/${documentNo}/`)
        .then(response => response.json())
        .then(data => {
            // Populate the modal with the new data
            document.getElementById('t_documentTrackingNumber').textContent = data.tracking_no;
            document.getElementById('t_documentSender').textContent = data.sender_name;
            document.getElementById('t_documentStatus').textContent = data.status;
            document.getElementById('t_documentType').textContent = data.document_type.charAt(0).toUpperCase() + data.document_type.slice(1)
            document.getElementById('t_documentPriority').textContent = data.priority;

            if(data.due_in > 1) {
                document.getElementById('t_documentDueIn').textContent = data.due_in + " Days";
            } else  {
                document.getElementById('t_documentDueIn').textContent = data.due_in + " Day";
            }
    
            document.getElementById('t_documentSubject').textContent = data.subject;
            
            const activitiesTableBody = document.getElementById('t_activitiesTableBody');
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
                    <td>${activity.activity}</td>
                `;

                activitiesTableBody.appendChild(row);
            });
            
            document.getElementById('t_documentTitleLink').setAttribute('data-document-no', documentNo); 
            // Hide spinner and show content once data is loaded
            document.getElementById('t_loadingSpinner').style.display = 'none';
            document.getElementById('t_documentDetailsContent').style.display = 'flex';
            document.getElementById('t_activitiesContent').style.display = 'flex';
           
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('t_loadingSpinner').style.display = 'none';
        });
});