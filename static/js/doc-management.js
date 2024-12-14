function fetchDocumentTypes() {

    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = document.getElementById('searchInput');
    let searchValue = searchQuery.value.trim();
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
            /*
                document.getElementById('docTableBody').innerHTML = data.html;
                let noOfRecords = document.getElementById('docuLength').value;
                document.getElementById('recordCount').textContent = noOfRecords;
                bindViewButtons();
            */
    });
}

function editDocumentType() {

    const editModal = document.getElementById('editDocumentTypeModal');
    const editDocumentNo = document.getElementById('editDocumentNo');
    const editDocumentType = document.getElementById('editDocumentType');
    const editCategory = document.getElementById('editCategory');
    const editPriorityLevel = document.getElementById('editPriorityLevel');
    const editRouteStepsContainer = document.getElementById('edit-route-steps-container');

    editModal.addEventListener('show.bs.modal', function (event) {
        
        const button = event.relatedTarget;
        const documentNo = button.getAttribute('data-document-no');
        const documentType = button.getAttribute('data-document-type');
        const category = button.getAttribute('data-category');
        const priorityLevel = button.getAttribute('data-priority-level');
        const routes = button.getAttribute('data-routes').split(',');

        // Populate the form with the document details
        editDocumentNo.value = documentNo;
        editDocumentType.value = documentType;
        editCategory.value = category;
        if(priorityLevel === 'Very urgent') {
            editPriorityLevel.value = 'Very Urgent';
        } else {
            editPriorityLevel.value = priorityLevel;
        }
        
        // Clear existing route steps and repopulate
        editRouteStepsContainer.innerHTML = '';  // Clear previous routes
        routes.forEach((route, index) => {
            const routeStep = document.createElement('div');
            routeStep.classList.add('input-group', 'm-0', 'edit-route-step');
            routeStep.innerHTML = `
                <span class="input-group-text">Route ${index + 1}</span>
                <select class="form-select edit-route-select" name="editRoutes[]" required>
                    <option value="" disabled hidden></option>
                    <option value="Director" ${route === 'Director' ? 'selected' : ''}>Director</option>
                    <option value="Accounting" ${route === 'Accounting' ? 'selected' : ''}>Accounting</option>
                    <option value="Budgeting" ${route === 'Budgeting' ? 'selected' : ''}>Budgeting</option>
                    <option value="Cashier" ${route === 'Cashier' ? 'selected' : ''}>Cashier</option>
                    <option value="Payroll" ${route === 'Payroll' ? 'selected' : ''}>Payroll</option>
                </select>
                <a href="#" class="btn btn-danger btn-x-red edit-remove-route-step"><i class="fa-solid fa-trash-can"></i></a>
            `;
            editRouteStepsContainer.appendChild(routeStep);
        });
    });

}

function deleteDocumentType() {

    deleteModal = document.getElementById('deleteDocumentTypeModal');
    confirmDeleteBtn = document.getElementById('confirmDelete');

    deleteModal.addEventListener('show.bs.modal', function (event){
        const button = event.relatedTarget;
        const documentNo = button.getAttribute('data-document-no');
        const url = button.getAttribute('data-url').replace(0, documentNo);

        confirmDeleteBtn.onclick = function () {
            window.location.href = url;
        }
    });

}

document.addEventListener('DOMContentLoaded', function() {
    fetchDocumentTypes();
    editDocumentType();
    deleteDocumentType();
    setInterval(fetchDocumentTypes, 3000);
});