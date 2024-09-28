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

                    if(data.due_in > 1) {
                        document.getElementById('documentDueIn').textContent = data.due_in + " Days";
                    } else  {
                        document.getElementById('documentDueIn').textContent = data.due_in + " Day";
                    }
            
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
                            <td>${activity.activity}</td>
                        `;

                        activitiesTableBody.appendChild(row);
                    });
                    
                    document.getElementById('documentTitleLink').setAttribute('data-document-no', documentNo); 

                })
                .catch(error => console.error('Error:', error));
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchDocuments();
    setInterval(fetchDocuments, 3000);
});