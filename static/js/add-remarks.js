function addRemarks() {
    const addRemarksBtn = document.getElementById('saveRemarks');
    addRemarksBtn.addEventListener('click', function() {

        const remarksInput = document.getElementById('remarks').value;

        const documentNo = addRemarksBtn.getAttribute('data-document-no');
        const remarksNo = addRemarksBtn.getAttribute('data-remarks-no');

        fetch(`/add-remarks/${documentNo}/${remarksNo}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Sending JSON data
                'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included for security
            },
            body: JSON.stringify({ remarksInput }),
        })
            .then(response => response.json())
            .then(status => {
                document.getElementById('remarks').value = '';
            })
            .catch(error => console.error('Error', error));
    });

    function getCSRFToken() {
        const name = 'csrftoken';
        const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name)).split('=')[1];
        return cookieValue;
    }
}

function deleteEmptyRemarks() {
    fetch(`/delete-empty-remarks/`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    addRemarks();
    eleteEmptyRemarks();
});