function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name)).split('=')[1];
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    
    const editRoutesModal = new bootstrap.Modal(document.getElementById('editDocumentRouteModal'));

    const rerouteButtons = document.querySelectorAll('.reroutebtn');
    const editRouteStepsContainer = document.getElementById('edit-route-steps-container');
    const editPriorityLevel = document.getElementById('editPriorityLevel');

    document.addEventListener('click', function (event) {
        if (event.target.closest('.reroutebtn')) {
            const button = event.target.closest('.reroutebtn');
            const documentNo = button.getAttribute('data-document-no');
            const documentType = button.getAttribute('data-document-type');
            const documentCategory = button.getAttribute('data-document-category');

            document.getElementById('editDocumentNo').value = documentNo;
            document.getElementById('documentTypeInput').value = documentType;
            document.getElementById('documentCategoryInput').value = documentCategory;
            

            fetch(`/fetch-document-routes/${documentNo}/`)
                .then(response => response.json())
                .then(data => {
                    
                    editRouteStepsContainer.innerHTML = ''; 
                    data.routes.forEach((route, index) => {
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

                    editPriorityLevel.value = data.priority_level

                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });

    document.getElementById('updateRoutesBtn').addEventListener('click', function() {

        editRoutesModal.hide();

        const form = document.getElementById('editDocumentTypeForm');
        const formData = new FormData(form);

        fetch('/edit-routes/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken(), 
            }
        })
        .then(response => response.json())
        .then(data => {
           console.log("routes edited");
        })
        .catch(error => console.error('Error', error));

    });
});

let editRouteStepCount = 1;

        // Add a new route step only if the current step has a selected value
        document.getElementById('edit-add-route-step').addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the link from navigating
            
            // Get the last select element
            const editLastRouteStep = document.querySelector('#edit-route-steps-container .edit-route-step');
            console.log("last route ng kineme: " + editLastRouteStep);
            // Check if the last select has a value selected
            if (editLastRouteStep && editLastRouteStep.value !== "") {
                editRouteStepCount++;
                const routeStepsContainer = document.getElementById('edit-route-steps-container');

                // Create a new div for the route step
                const newRouteStep = document.createElement('div');
                newRouteStep.classList.add('input-group', 'm-0', 'edit-route-step');

                // Set the inner HTML for the new route step
                newRouteStep.innerHTML = `
                    <span class="input-group-text">Route ${editRouteStepCount}</span>
                    <select class="form-select edit-route-select" name="editRoutes[]" required>
                        <option value="" disabled selected hidden>Select Office</option>
                        <option value="Director">Director</option>
                        <option value="Accounting">Accounting</option>
                        <option value="Budgeting">Budgeting</option>
                        <option value="Cashier">Cashier</option>
                        <option value="Payroll">Payroll</option>
                    </select>
                    <a href="#" class="btn btn-danger btn-x-red edit-remove-route-step"><i class="fa-solid fa-trash-can"></i></a>
                `;

                // Append the new route step to the container
                routeStepsContainer.appendChild(newRouteStep);

                // Update the available options for the new select element
                editUpdateRouteOptions();
            } else {
                // Create a Bootstrap alert
                const alertContainer = document.getElementById('alert-container-edit');
                const alert = document.createElement('div');
                alert.classList.add('alert', 'alert-warning', 'alert-dismissible', 'fade', 'show');
                alert.role = 'alert';
                alert.innerHTML = `
                    Please select an office before adding a new step.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                `;
                alertContainer.appendChild(alert);
s
                // Optional: Automatically remove the alert after a few seconds
                setTimeout(() => {
                    alert.classList.remove('show');
                    alert.addEventListener('transitionend', () => alert.remove());
                }, 3000); // Alert will auto-close after 3 seconds
            }
        });

        // Remove a route step and update the numbering and available options
        document.addEventListener('click', function(e) {
            if (e.target && e.target.closest('.edit-remove-route-step')) {
                e.preventDefault(); // Prevent link navigation
                const routeStep = e.target.closest('.edit-route-step');
                
                if (routeStep.querySelector('.input-group-text').textContent === 'Route 1') {
                    const selectElement = routeStep.querySelector('.form-select');
                    if (selectElement.value) {
                        selectElement.value = ""; // Reset the value to placeholder if an option is selected
                    }
                } else {
                    routeStep.remove();
                    editUpdateRouteStepNumbers();
                    editUpdateRouteOptions();
                }
            }
        });

        // Function to update step numbers after removal
        function editUpdateRouteStepNumbers() {
            const routeSteps = document.querySelectorAll('.edit-route-step');
            editRouteStepCount = routeSteps.length;
            routeSteps.forEach((step, index) => {
                const stepLabel = step.querySelector('.input-group-text');
                stepLabel.textContent = `Route ${index + 1}`;
            });
        }

        // Function to update the available options for each route select element
        function editUpdateRouteOptions() {
            let editPreviousSelected = "";
            const routeSteps = document.querySelectorAll('.edit-route-step select');
             // Store the previously selected department

            routeSteps.forEach((select, index) => {
                const editCurrentSelected = select.value;
                let isValidSelection = false; // Flag to check if the current selection is valid

                // Clear all options and re-add them
                const options = ['Director', 'Accounting', 'Budgeting', 'Cashier', 'Payroll'];
                select.innerHTML = '<option value="" disabled selected hidden>Select Office</option>';

                options.forEach(option => {
                    if (index === 0 || option !== editPreviousSelected) {
                        const optionElement = document.createElement('option');
                        optionElement.value = option;
                        optionElement.textContent = option;

                        // Add option element to the select
                        select.appendChild(optionElement);

                        // Check if the current selected value is still a valid option
                        if (option === editCurrentSelected) {
                            isValidSelection = true;
                        }
                    }
                });

                // Set the previously selected department for the next step
                editPreviousSelected = editCurrentSelected;

                // Re-select the current value if it is still valid, otherwise reset to placeholder
                if (isValidSelection) {
                    select.value = editCurrentSelected;
                } else {
                    select.value = ""; // Reset to the placeholder
                }
            });
        }