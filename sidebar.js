document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('menuToggle');  // Ensure this button exists
    const mainContent = document.getElementById('mainContent');
    const navLinks = document.querySelectorAll('.nav-link[data-link]');
    const ajaxTarget = document.getElementById('ajaxContent');  // Ensure ajaxContent exists

    // Sidebar toggle
    if (toggle) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Auto-collapse sidebar on nav click (mobile)
    navLinks.forEach(link => {
        if (window.innerWidth <= 768) {
            link.addEventListener('click', () => {
                sidebar.classList.remove('active');
            });
        }
    });

    // Active link highlighting
    navLinks.forEach(link => {
        const current = window.location.pathname;
        if (link.getAttribute('href') === current) {
            link.classList.add('active');
        }
    });

    // SPA AJAX loading (optional, fallback-safe)
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            fetch(url)
                .then(res => res.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#ajaxContent');
                    if (newContent) {
                        ajaxTarget.innerHTML = newContent.innerHTML;
                        window.history.pushState({}, '', url);
                        // Rerun highlighting
                        navLinks.forEach(link => link.classList.remove('active'));
                        this.classList.add('active');
                        // Collapse sidebar if mobile
                        if (window.innerWidth <= 768) {
                            sidebar.classList.remove('active');
                        }
                    } else {
                        window.location.href = url; // fallback if AJAX fails
                    }
                });
        });
    });
});
