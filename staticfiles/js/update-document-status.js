document.addEventListener('DOMContentLoaded', function () {
    const modals = {
        route: document.getElementById('routeDocumentModal'),
        approve: document.getElementById('approveDocumentModal'),
        reject: document.getElementById('rejectDocumentModal'),
        forward: document.getElementById('forwardDocumentModal'),
        endorse: document.getElementById('endorseDocumentModal'),
        resolve: document.getElementById('resolveDocumentModal'),
        archive: document.getElementById('archiveDocumentModal'),
        delete: document.getElementById('deleteDocumentModal'),
    };

    const confirmButtons = {
        route: document.getElementById('confirmRoute'),
        approve: document.getElementById('confirmApprove'),
        reject: document.getElementById('confirmReject'),
        forward: document.getElementById('confirmForward'),
        resolve: document.getElementById('confirmResolve'),
        endorse: document.getElementById('confirmEndorse'),
        archive: document.getElementById('confirmArchive'),
        delete: document.getElementById('confirmDelete'),
    };

    for (const [action, modal] of Object.entries(modals)) {
        if (modal) {
            modal.addEventListener('show.bs.modal', function (event) {
                const button = event.relatedTarget;
                if (!button) {
                    console.error('No button element triggered the modal.');
                    return;
                }
                const documentNo = button.getAttribute('data-document-no');
                const actionType = button.getAttribute('data-action'); // Changed from 'action' to 'actionType'
                
                if (confirmButtons[actionType]) {
                    confirmButtons[actionType].onclick = function () {
                        fetch(`/document-update-status/${action}/${documentNo}/`)
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('saveRemarks').setAttribute('data-remarks-no', data.remarks_no);
                                document.getElementById('saveRemarks').setAttribute('data-document-no', documentNo);
                                document.getElementById('saveRemarks').removeAttribute('data-activity-log-no');
                                console.log(data.activity_log_no);
                                document.getElementById('saveRemarks').setAttribute('data-activity-log-no', data.activity_log_no);
                            })
                            .catch(error => console.error('Error', error));
                    };
                }
            });
        }
    }
});
