// JavaScript to update profile picture preview and ensure file is correctly linked
document.getElementById('changePhotoInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Update the profile picture preview
            document.getElementById('editProfilePicture').src = e.target.result;
        };
        reader.readAsDataURL(file);
        
        // Link the file to the hidden input to ensure it gets submitted
        document.getElementById('profilePictureInput').files = event.target.files;
    }
});


document.getElementById('deletePhotoButton').addEventListener('click', function() {
    // Update the profile picture to the default image
    document.getElementById('editProfilePicture').src = '/attachments/profile_pics/default_profile_pic.png';
    document.getElementById('profilePictureInput').value = '';

    // Add a hidden input to indicate the deletion
    if (!document.getElementById('deletePhotoInput')) {
        const deleteInput = document.createElement('input');
        deleteInput.type = 'hidden';
        deleteInput.name = 'delete_photo';
        deleteInput.id = 'deletePhotoInput';
        deleteInput.value = '1'; // Value to indicate photo deletion
        document.getElementById('editProfileForm').appendChild(deleteInput);
    }
});
