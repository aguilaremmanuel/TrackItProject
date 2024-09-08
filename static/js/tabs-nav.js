document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabs.forEach(tab => {
        tab.addEventListener('click', function(event) {
            event.preventDefault();

            // Remove 'active' class from all tabs and tab panes
            tabs.forEach(t => t.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            // Add 'active' class to the clicked tab and the corresponding pane
            this.classList.add('active');
            const targetPaneId = this.getAttribute('href').substring(1);
            document.getElementById(targetPaneId).classList.add('active');
        });
    });
});