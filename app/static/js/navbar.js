/*Set the class of a navbar list item to "active" if the list item id is equal to the second word in <title> tag*/
function setActiveNavbar () {
    const pageName = document.title.split(' ')[1];
    const navbarItem = document.getElementById(pageName);
    if (navbarItem !== null) {
    navbarItem.className = "active";
    }
}
setActiveNavbar();

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

//When object in window is clicked, if object isn't part of a dropdown, hide dropdowns
window.addEventListener("click", (e) => {
    const loginDropdown = document.getElementById('loginDropdown');
    const signupDropdown = document.getElementById('signupDropdown');
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');

    // If the click is not inside the login or signup dropdown, close them
    if (!loginDropdown.contains(e.target) && !loginBtn.contains(e.target)) {
        loginDropdown.style.display = 'none';
    }
    if (!signupDropdown.contains(e.target) && !signupBtn.contains(e.target)) {
        signupDropdown.style.display = 'none';
    }
})

//Event handlers for login and signup buttons
document.getElementById("loginBtn").addEventListener("click", function(e) {
    e.stopPropagation(); // Prevent the window click listener from firing
    // Hide signup if it's open
    document.getElementById("signupDropdown").style.display = "none";
    // Toggle login
    toggleVisible("loginDropdown");
});

document.getElementById("signupBtn").addEventListener("click", function(e) {
    e.stopPropagation(); // Prevent the window click listener from firing
    // Hide login if it's open
    document.getElementById("loginDropdown").style.display = "none";
    // Toggle signup
    toggleVisible("signupDropdown");
});

// Show login or signup dropdown after reload if error flag is passed in the DOM
document.addEventListener("DOMContentLoaded", () => {
    const dropdownToShow = document.body.dataset.showDropdown;
    if (dropdownToShow === "login") {
        document.getElementById("loginDropdown").style.display = "block";
        document.getElementById("signupDropdown").style.display = "none";
    } else if (dropdownToShow === "signup") {
        document.getElementById("signupDropdown").style.display = "block";
        document.getElementById("loginDropdown").style.display = "none";
    }
});