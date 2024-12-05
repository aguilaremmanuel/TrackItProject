document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const container = document.querySelector('.container');
    const toggleButton = document.getElementById('toggleSidebar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navLogo = document.querySelector('.nav-logo');
    const mainContent = document.querySelector('.main-content');
    const header = document.querySelector('.header');

    // Function to adjust header padding based on scroll
    function adjustHeaderPadding() {
        if (mainContent.scrollHeight > mainContent.clientHeight) {
            // If main-content has vertical scroll
            header.style.paddingRight = '2.55rem'; // Original padding + 0.8rem
        } else {
            // If no vertical scroll
            header.style.paddingRight = '1.75rem';
        }
    }

    // Sidebar toggle logic
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

    // Adjust header padding on page load
    adjustHeaderPadding();

    // Observe main-content for size changes
    new ResizeObserver(adjustHeaderPadding).observe(mainContent);
});
