function toggleVisible(dropdownId) {
    const dropdown = document.getElementById(dropdownId);

    document.querySelectorAll('.dropdown-content').forEach(container => {
        if (container.id !== dropdownId) {
            container.style.display = 'none';
        }
    });
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
document.getElementById("loginBtn").addEventListener("click", function() {toggleVisible("loginDropdown"); });
document.getElementById("signupBtn").addEventListener("click", function() {toggleVisible("signupDropdown"); });