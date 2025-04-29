function toggleVisible(dropdownId) {
    const dropdown = document.getElementById(dropdownId);

    document.querySelectorAll('.dropdown-content').forEach(container => {
        if (container.id !== dropdownId) {
            container.style.display = 'none';
        }
    });
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

window.addEventListener("click", (e) => {
    let parent = e.target.parentNode;
    while (parent.nodeName !== "HTML") {
        if (parent.className.split(' ').includes("dropdown")) {
            return;
        }
        parent = parent.parentNode;
    }
    
    if (!e.target.parentNode.matches('.dropdown')) {
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

document.getElementById("loginBtn").addEventListener("click", function() {toggleVisible("loginDropdown"); });
document.getElementById("signupBtn").addEventListener("click", function() {toggleVisible("signupDropdown"); });