document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dropdown-toggle').forEach((dropdownToggle) => {
        dropdownToggle.addEventListener('click', (event) => {
            event.preventDefault();
            const dropdownMenu = dropdownToggle.nextElementSibling;
            dropdownMenu.classList.toggle('show');
        });
    });
});