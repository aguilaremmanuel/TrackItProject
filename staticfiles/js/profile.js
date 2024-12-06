function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const editProfilePicture = document.getElementById('editProfilePicture');
            editProfilePicture.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name)).split('=')[1];
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {

    const editProfileModal = new bootstrap.Modal(document.getElementById('editProfileModal'),{
        backdrop: 'static',
        keyboard: false
    });

    document.getElementById('saveEditProfileBtn').addEventListener('click', function() {

        const form = document.getElementById('editProfileForm');
        const formData = new FormData(form);

        if (form.checkValidity()) {

            fetch('/edit-profile/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken(), 
                }
            })
                .then(response => response.json())
                .then(status => {
                    editProfileModal.hide();
                })
                .catch(error => console.error('Error', error));

        } else {
            form.reportValidity();
        }

    });

});

function editProfile() {

    const form = document.getElementById('editProfileForm');
    const formData = new FormData(form);

    fetch(`/add-remarks/${documentNo}/${remarksNo}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken(), // Ensure CSRF token is included for security
        }
    })
        .then(response => response.json())
        .then(status => {
            document.getElementById('remarks').value = '';
        })
        .catch(error => console.error('Error', error));
}