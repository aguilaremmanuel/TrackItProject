document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const container = document.querySelector('.container');
    const toggleButton = document.getElementById('toggleSidebar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navLogo = document.querySelector('.nav-logo');

    toggleButton.addEventListener('click', () => {
        if (sidebar.classList.contains('collapsed')) {
            // Expand the sidebar and remove collapsed class
            container.style.setProperty('--sidebar-width', '225px');
            sidebar.classList.remove('collapsed');
            
            // Remove collapsed class from nav-logo and each nav-link
            navLogo.classList.remove('collapsed');
            navLinks.forEach(link => {
                link.classList.remove('collapsed');
                // Remove tooltip on expand
                link.removeAttribute('title');
            });
        } else {
            // Collapse the sidebar and add collapsed class
            container.style.setProperty('--sidebar-width', '66px');
            sidebar.classList.add('collapsed');

            // Add collapsed class to nav-logo and each nav-link
            navLogo.classList.add('collapsed');
            navLinks.forEach(link => {
                link.classList.add('collapsed');
                // Set the title for the tooltip
                link.setAttribute('title', link.querySelector('.nav-name').textContent);
            });
        }
    });
});
