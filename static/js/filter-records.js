const filterButton = document.getElementById("filterButton");
const filterDropdown = document.querySelector(".drop-filter");

document.getElementById('applyFilterBtn').addEventListener('click', function() {

    const status = Array.from(document.querySelectorAll('input[name="status"]:checked'))
                .map(checkbox => checkbox.value);
    const type = Array.from(document.querySelectorAll('input[name="type"]:checked'))
                .map(checkbox => checkbox.value);
    const priority = Array.from(document.querySelectorAll('input[name="priority"]:checked'))
                .map(checkbox => checkbox.value);

    console.log(status);
    console.log(type);
    console.log(priority);
                
    const filterData = {
        status: status.length > 0 ? status : [],
        type: type.length > 0 ? type : [],
        priority: priority.length > 0 ? priority : []
    };

    fetch('/filter-records/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
        },
        body: JSON.stringify(filterData)
    })
    .then(response => response.json())
    .then(data => {
        filterDropdown.classList.remove("show");
        filterButton.setAttribute("aria-expanded", "false");
    })
    .catch(error => {
        console.error('Error:', error);
    });

});

const resetFiltersBtn = document.getElementById("resetFilters");
resetFiltersBtn.addEventListener("click", function () {

    const checkboxes = document.querySelectorAll(".drop-filter input[type='checkbox']");
    checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
    });

    fetch('/remove-filter/')
    .then(response => response.json())
    .then(data => {
        console.log("success");
    })
    .catch(error => {
        console.error('Error:', error);
    });

}); 

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}