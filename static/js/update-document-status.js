document.addEventListener('DOMContentLoaded', function () {
    const modals = {
        route: document.getElementById('routeDocumentModal'),
        approve: document.getElementById('approveDocumentModal'),
        forwardToACT: document.getElementById('forwardToACTDocumentModal'),
        endorseResolve: document.getElementById('endorseResolveDocumentModal'),
        resolve: document.getElementById('resolveDocumentModal'),
        archive: document.getElementById('archiveDocumentModal')
    };

    const confirmButtons = {
        route: document.getElementById('confirmRoute'),
        approve: document.getElementById('confirmApprove'),
        forwardToACT: document.getElementById('confirmForwardToACT'),
        resolve: document.getElementById('confirmResolve'),
        archive: document.getElementById('confirmArchive')
    };

    for (const [action, modal] of Object.entries(modals)) {
        if (modal) {
            modal.addEventListener('show.bs.modal', function (event) {
                const button = event.relatedTarget;
                const documentNo = button.getAttribute('data-document-no');
                const actionType = button.getAttribute('data-action'); // Changed from 'action' to 'actionType'

                if (confirmButtons[actionType]) {
                    confirmButtons[actionType].onclick = function () {
                        fetch(`/document-update-status/${action}/${documentNo}/`)
                            .then(response => response.json())
                            .then(data => {
                                document.getElementById('saveRemarks').setAttribute('data-remarks-no', data.remarks_no);
                                document.getElementById('saveRemarks').setAttribute('data-document-no', documentNo);
                            })
                            .catch(error => console.error('Error', error));
                    };
                }
            });
        }
    }
});
