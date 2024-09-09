document.addEventListener("DOMContentLoaded", function(event) {
    const toggleId = 'headerToggle';
    const navId = 'navBar';
    const bodyId = 'bodyPd';
    const headerId = 'header';

    const toggle = document.getElementById(toggleId);
    const nav = document.getElementById(navId);
    const bodypd = document.getElementById(bodyId);
    const headerpd = document.getElementById(headerId);

    // Retrieve the sidebar state from local storage
    const sidebarState = localStorage.getItem('sidebarState');
    if (sidebarState === 'expanded') {
        nav.classList.add('show-sidebar');
        toggle.classList.add('bx-x');
        bodypd.classList.add('body-pd');
        headerpd.classList.add('body-pd');
        hideNavText(false); // Show text when expanded
        adjustNavLinkGap(false); // No gap when expanded
    } else {
        nav.classList.remove('show-sidebar');
        toggle.classList.remove('bx-x');
        bodypd.classList.remove('body-pd');
        headerpd.classList.remove('body-pd');
        hideNavText(true); // Hide text when collapsed
        adjustNavLinkGap(true); // No gap when collapsed
    }

    // Toggle the sidebar state and save it to local storage
    if (toggle) {
        toggle.addEventListener('click', () => {
            const isExpanded = nav.classList.toggle('show-sidebar');
            toggle.classList.toggle('bx-x');
            bodypd.classList.toggle('body-pd');
            headerpd.classList.toggle('body-pd');
            hideNavText(!isExpanded); // Toggle text visibility based on state
            adjustNavLinkGap(!isExpanded); // Adjust column gap based on state
            
            // Save the sidebar state to local storage
            localStorage.setItem('sidebarState', isExpanded ? 'expanded' : 'collapsed');
        });
    }

    // Function to hide or show nav text
    function hideNavText(hide) {
        const logoName = document.querySelector('.nav-logo-name');
        const navNames = document.querySelectorAll('.nav-name');
        
        if (hide) {
            logoName.style.display = 'none';
            navNames.forEach(name => name.style.display = 'none');
        } else {
            logoName.style.display = 'block';
            navNames.forEach(name => name.style.display = 'block');
        }
    }

    // Function to adjust the column-gap of nav-link
    function adjustNavLinkGap(collapse) {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.style.columnGap = collapse ? '0' : '1.1rem'; // Set gap to 0 when collapsed
        });
    }

    const linkColor = document.querySelectorAll('.nav-link');
    function colorLink() {
        linkColor.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    }

    linkColor.forEach(l => l.addEventListener('click', colorLink));
});