document.getElementById("addBtn").addEventListener("click", function() {toggleVisible("addDropdown"); });

//When object in window is clicked, if object isn't part of a dropdown, hide dropdowns
window.addEventListener("click", (e) => {
    const addBtn = document.getElementById('addBtn');
    const addDropdown = document.getElementById('addDropdown');

    // If the click is not inside the login or signup dropdown, close them
    if (!addDropdown.contains(e.target) && !addBtn.contains(e.target)) {
        addDropdown.style.display = 'none';
    }
})