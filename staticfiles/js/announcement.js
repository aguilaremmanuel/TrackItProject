//disable date in calendar if past
document.addEventListener('DOMContentLoaded', function() {
    // Helper function to set min date
    function setMinDate(inputId) {
        const dateInput = document.getElementById(inputId);
        const today = new Date();
        
        // Format today's date as YYYY-MM-DD
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        const dd = String(today.getDate()).padStart(2, '0');
        
        const formattedDate = `${yyyy}-${mm}-${dd}`;
        
        // Set the min attribute
        dateInput.setAttribute('min', formattedDate);
    }

    // Set min date for both inputs
    setMinDate('endDate');
    setMinDate('editAnnouncementEndDate');
});


// Function to open and populate the Edit Modal
function openEditModal(id, title, description, attachmentUrl, endDate) {
    // Set the values in the modal
    document.getElementById('announcementId').value = id;
    document.getElementById('editAnnouncementTitle').value = title;  // Set the title in the textarea
    document.getElementById('announcementDescription').value = description;
    document.getElementById('editAnnouncementEndDate').value = endDate; //  

    // Handle existing attachment
    //const existingAttachmentElement = document.getElementById('existingAttachment');
    //if (attachmentUrl) {
    //    existingAttachmentElement.innerHTML = `<a href="${attachmentUrl}" target="_blank">View existing attachment</a>`;
    //} else {
    //    existingAttachmentElement.innerHTML = 'No attachment available.';
    //}
    //console.log("End Date:", endDate); // This will print the endDate value
    
    // Show the modal
    var editModal = new bootstrap.Modal(document.getElementById('editAnnouncementModal'));
    editModal.show();
}

// Handle form submission with AJAX and file upload
document.getElementById('editAnnouncementForm').onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    
    const id = document.getElementById('announcementId').value;
    const atitle = document.getElementById('editAnnouncementTitle').value;
    const description = document.getElementById('announcementDescription').value;
    const attachment = document.getElementById('announcementAttachment').files[0];
    const endDate = document.getElementById('editAnnouncementEndDate').value; //

    const formData = new FormData();
    formData.append('title', atitle);
    formData.append('description', description);
    if (attachment) {
        formData.append('attachment', attachment); // Attach the new file if provided
    }
    formData.append('end_date', endDate); // Include end date in form data

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Make an AJAX request to update the announcement
    fetch(`/update-announcement/${id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData // Send the form data with the file
    })
    .then(response => {
        if (response.ok) {
            location.reload();  // Reload to see the changes
        } else {
            alert('Failed to update announcement.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function deleteAnnouncement(button, id) {
    // Create a custom confirmation dialog
    const confirmation = confirm("Are you sure you want to delete this announcement?");
    
    if (confirmation) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/delete-announcement/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                // Select the entire parent container that includes both the record and the button
                const announcementElement = button.closest('.d-flex');
                // Remove both the record and the button
                announcementElement.remove();
                alert('Announcement deleted successfully.');
            } else {
                alert('Failed to delete announcement.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

let deleteAnnouncementId = null;  // Store the ID of the announcement to be deleted

function deleteAnnouncement(button, id) {
    // Set the ID of the announcement to be deleted
    deleteAnnouncementId = id;

    // Show the confirmation modal
    const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
    confirmationModal.show();
}

// Bind the "Delete" button inside the modal
document.getElementById('confirmDeleteBtn').addEventListener('click', function() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Make the POST request to delete it from the server
    fetch(`/delete-announcement/${deleteAnnouncementId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'  // Ensure the body is sent as JSON
        },
        body: JSON.stringify({ id: deleteAnnouncementId })  // Send the ID as JSON data
    })
    .then(response => {
        if (response.ok) {
            // Get the announcement record to be deleted and remove it from the DOM
            const announcementElement = document.querySelector(`[data-id="${deleteAnnouncementId}"]`).closest('.d-flex');
            announcementElement.remove();

            // Hide the confirmation modal
            const confirmationModal = bootstrap.Modal.getInstance(document.getElementById('confirmationModal'));
            confirmationModal.hide();

            // Show the success message inside the form
            const successMessage = document.getElementById('successMessage');
            successMessage.style.display = 'block';  // Make the success message visible

            // Hide the success message after 3 seconds
            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 3000);
        } else {
            alert('Failed to delete announcement.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function viewFile(fileName) {
    const pdfFileUrl = `/attachments/${fileName}`; 
    const originalFileUrl = `/attachments/${fileName}`; 
    
    fetch(pdfFileUrl, { method: 'HEAD' })
        .then(response => {
            const fileUrl = response.ok ? pdfFileUrl : originalFileUrl;
            document.getElementById('attachmentViewer').src = fileUrl;
            const attachmentModal = new bootstrap.Modal(document.getElementById('attachmentModal'));
            attachmentModal.show();
        })
        .catch(error => {
            console.error("Error loading file:", error);
        });
}
