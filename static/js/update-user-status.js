document.addEventListener('DOMContentLoaded', function () {
    const modals = {
        verify: document.getElementById('verifyUserModal'),
        reject: document.getElementById('rejectUserModal'),
        deactivate: document.getElementById('deactivateUserModal'),
        archive: document.getElementById('archiveUserModal'),
        reactivate: document.getElementById('reactivateUserModal')
    };

    const confirmButtons = {
        verify: document.getElementById('confirmVerify'),
        reject: document.getElementById('confirmReject'),
        deactivate: document.getElementById('confirmDeactivate'),
        archive: document.getElementById('confirmArchive'),
        reactivate: document.getElementById('confirmReactivate')
    };

    for (const [action, modal] of Object.entries(modals)) {
        modal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const userId = button.getAttribute('data-user-id');
            const actionType = button.getAttribute('data-action');
            
            const url = button.getAttribute('data-url').replace('USER_ID', userId).replace('ACTION_TYPE', actionType);

            confirmButtons[actionType].onclick = function () {

                const bootstrapModal = bootstrap.Modal.getInstance(modal); // Get the Bootstrap modal instance
                bootstrapModal.hide(); // Close the modal
                window.location.href = url;
      

            };
        });
    }
});
