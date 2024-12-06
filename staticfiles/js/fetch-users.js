function fetchUsers() {

    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = document.getElementById('searchInput');
    let searchValue = searchQuery.value.trim().replace(/\s+/g, '');
    let updateUrl = searchQuery.getAttribute('data-url');
    let fetchUrl = updateUrl + `?search=${encodeURIComponent(searchValue)}`;
    // Include sorting parameters only if searchQuery is empty
    if (!searchValue) {
        const sortBy = urlParams.get('sort_by') || '';
        const order = urlParams.get('order') || 'asc';
        fetchUrl = updateUrl + "?sort_by=" + sortBy + "&order=" + order;
    }

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            
            document.getElementById('userTableBody').innerHTML = data.html;
            let noOfRecords = document.getElementById('userLength').value;
            document.getElementById('recordCount').textContent = noOfRecords;
    });

}

document.addEventListener('DOMContentLoaded', function() {
    fetchUsers();
    setInterval(fetchUsers, 3000);
});
