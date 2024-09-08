const tableBodies = document.querySelectorAll('.tab-pane.active tbody');
tableBodies.forEach((tbody) => {
    const recordCountElement = document.getElementById('record-count');
    const rowCount = tbody.querySelectorAll('tr').length;
    recordCountElement.textContent = `Showing total of ${rowCount} record(s)`;
});

/* TEST COMMIT */