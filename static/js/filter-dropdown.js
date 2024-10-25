// Prevent dropdown from closing when clicking on form-check elements
document.querySelectorAll('.form-check-input, .form-check-label').forEach((element) => {
    element.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevents the dropdown from closing
    });
});

// Prevent dropdown from closing when clicking inside the dropdown menu
document.querySelectorAll('.drop-filter').forEach((dropdown) => {
    dropdown.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevents the dropdown from closing
    });
});

// Reset button functionality
document.getElementById('resetFilters').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent any default action
    event.stopPropagation(); // Prevent the dropdown from closing

    // Uncheck all checkboxes
    document.querySelectorAll('.form-check-input').forEach((checkbox) => {
        checkbox.checked = false;
    });

    // Dropdown remains open
});