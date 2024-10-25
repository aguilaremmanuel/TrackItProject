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
            bindDownloadButtons();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetchReports();
    setInterval(fetchReports, 3000);
});

function bindDownloadButtons() {
    const downloadButtons = document.querySelectorAll('.downloadButton');

    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const reportNo = button.getAttribute('data-report-no');
            window.open(`/download-performance-report/${reportNo}`, '_blank');
        })
    });
}
