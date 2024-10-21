function fetchReports() {

    const searchQuery = document.getElementById('searchInput');
    let searchValue = searchQuery.value.trim();
    let updateUrl = searchQuery.getAttribute('data-url');
    let fetchUrl = updateUrl + `?search=${encodeURIComponent(searchValue)}`;

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            
            document.getElementById('reportsTableBody').innerHTML = data.html;
            let noOfRecords = document.getElementById('reportsCount').value;
            document.getElementById('recordCount').textContent = noOfRecords;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchReports();
    setInterval(fetchReports, 3000);
});
