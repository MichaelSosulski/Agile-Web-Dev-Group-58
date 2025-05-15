//Make dropdown with dropdownId visible, hide all other dropdowns
function toggleVisible(dropdownId) {
    const dropdown = document.getElementById(dropdownId);

    document.querySelectorAll('.dropdown-content').forEach(container => {
        if (container.id !== dropdownId) {
            container.style.display = 'none';
        }
    });
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}