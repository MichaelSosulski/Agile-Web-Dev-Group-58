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
    //Cancel handler if clicked inside of dropdown
    let parent = e.target.parentNode;
    while (parent.nodeName !== "HTML") {
        if (parent.className.split(' ').includes("dropdown")) {
            return;
        }
        parent = parent.parentNode;
    }
    //Checks if element pressed is not a child of an element of the dropdown class.
    if (!e.target.parentNode.matches('.dropdown')) {
        //hide .dropdown-contents
        let dropdowns = document.getElementsByClassName("dropdown-content");
        let i;
        for (i = 0; i < dropdowns.length; i++) {
          let openDropdown = dropdowns[i];
          if (openDropdown.style.display === "block") {
            openDropdown.style.display = "none";
          }
        }
      }
})

//Event handlers for login and signup buttons
document.getElementById("loginBtn").addEventListener("click", function() {toggleVisible("loginDropdown"); });
document.getElementById("signupBtn").addEventListener("click", function() {toggleVisible("signupDropdown"); });