document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const container = document.querySelector('.container');
    const toggleButton = document.getElementById('toggleSidebar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navLogo = document.querySelector('.nav-logo');
    const mainContent = document.querySelector('.main-content');
    const header = document.querySelector('.header');
    const navDropIcons = document.querySelectorAll('.nav-drop-icon');
    const submenus = document.querySelectorAll('[data-bs-toggle="collapse"]');

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

    // Function to expand the sidebar
    function expandSidebar() {
        if (sidebar.classList.contains('toggled')) {
            container.style.setProperty('--sidebar-width', '232px');
            sidebar.classList.remove('toggled');
            navLogo.classList.remove('toggled');
            navLinks.forEach(link => {
                link.classList.remove('toggled');
                link.removeAttribute('title');
            });
            navDropIcons.forEach(icon => {
                icon.classList.remove('toggled');
            });
        }
    }

    // Function to collapse the sidebar
    function collapseSidebar() {
        container.style.setProperty('--sidebar-width', '66px');
        sidebar.classList.add('toggled');
        navLogo.classList.add('toggled');
        navLinks.forEach(link => {
            link.classList.add('toggled');
            link.setAttribute('title', link.querySelector('.nav-name')?.textContent);
        });
        navDropIcons.forEach(icon => {
            icon.classList.add('toggled');
        });

        // Close all submenus
        submenus.forEach(submenu => {
            const target = document.querySelector(submenu.getAttribute('data-bs-target'));
            if (target && target.classList.contains('show')) {
                submenu.setAttribute('aria-expanded', 'false');
                target.classList.remove('show');
            }
        });
    }

    // Sidebar toggle logic
    toggleButton.addEventListener('click', () => {
        if (sidebar.classList.contains('toggled')) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    });

    // Expand sidebar when clicking on a nav-link with a submenu
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            // Check if the clicked nav-link has a submenu
            if (link.getAttribute('data-bs-toggle') === 'collapse') {
                expandSidebar();
            }
        });
    });

    // Adjust header padding on page load
    adjustHeaderPadding();

    // Observe main-content for size changes
    new ResizeObserver(adjustHeaderPadding).observe(mainContent);
});
