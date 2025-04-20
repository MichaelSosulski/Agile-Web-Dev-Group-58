function toggleVisible() {
    document.getElementById("myDropdown").classList.toggle("show");
}
document.getElementById("loginBtn").addEventListener("click", toggleVisible);

function dropForm(formId) {
    const dropdown = document.getElementById(formId);

    
    document.querySelectorAll('.form-container').forEach(container => {
        if (container.id !== formId) {
            container.style.display = 'none';
        }
    });

    // Toggle the selected dropdown
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
