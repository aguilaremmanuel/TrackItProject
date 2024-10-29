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
    const confirmUrgentDocModal = new bootstrap.Modal(document.getElementById('confirmUrgentDocModal'));
    const saveRemarksBtn =  document.getElementById('saveRemarks');
    saveRemarksBtn.addEventListener('click', function (e) {

        e.preventDefault();
        const documentNo = saveRemarksBtn.getAttribute('data-document-no');
        const remarksNo = saveRemarksBtn.getAttribute('data-remarks-no');

        const form = document.getElementById('remarksForm');
        const formData = new FormData(form);

        fetch(`/check-remarks/${documentNo}/${remarksNo}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(),  // Include the CSRF token in the request header
            }
        })
        .then(response => response.json())
        .then(data => {

            if(data.high_priority_detected) {
                document.getElementById('remarksDisplay').innerHTML = data.highlighted_remarks;
                document.getElementById('confirmChangePrioLevelBtn').setAttribute('data-document-no', documentNo);
                document.getElementById('confirmChangePrioLevelBtn').setAttribute('data-remarks-no', remarksNo);
                
                confirmUrgentDocModal.show();
            }

        })
        .catch(error => {
            console.error('Error:', error);
        });
    });    

    const confirmChangePrioLevelBtn =  document.getElementById('confirmChangePrioLevelBtn');
    confirmChangePrioLevelBtn.addEventListener('click', function () {
        
        confirmUrgentDocModal.hide();

        const documentNo = confirmChangePrioLevelBtn.getAttribute('data-document-no');
        const remarksNo = confirmChangePrioLevelBtn.getAttribute('data-remarks-no');

        fetch(`/change-priority-level/${documentNo}/${remarksNo}/`)
        .then(response => response.json())
        .then(data => {
            console.log(data.sucess);
        })
        .catch(error => console.error('Error', error));

    });

    deleteEmptyRemarks();
});

function deleteEmptyRemarks() {
    fetch(`/delete-empty-remarks/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}