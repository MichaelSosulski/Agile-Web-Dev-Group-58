// Ensure DOM content is loaded before executing scripts
document.addEventListener("DOMContentLoaded", function() {
    
    // Set active navbar item
    function setActiveNavbar() {
        const pageName = document.title.split(" ")[1];
        const navbarItem = document.getElementById(pageName);
        if (navbarItem) {
            navbarItem.className = "active";
        }
    }
    setActiveNavbar();

    // Dropdown handling
    function toggleVisible(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            document.querySelectorAll(".dropdown-content").forEach(container => {
                container.style.display = container.id !== dropdownId ? "none" : container.style.display === "block" ? "none" : "block";
            });
        }
    }

    window.addEventListener("click", (e) => {
        let parent = e.target.closest(".dropdown");
        if (!parent) {
            document.querySelectorAll(".dropdown-content").forEach(dropdown => {
                if (dropdown.style.display === "block") {
                    dropdown.style.display = "none";
                }
            });
        }
    });

    // Ensure login and signup buttons exist before adding event listeners
    const loginBtn = document.getElementById("loginBtn");
    const signupBtn = document.getElementById("signupBtn");

    if (loginBtn) {
        loginBtn.addEventListener("click", function() { toggleVisible("loginDropdown"); });
    }
    if (signupBtn) {
        signupBtn.addEventListener("click", function() { toggleVisible("signupDropdown"); });
    }

    // Enable horizontal scrolling for image selection
    document.querySelectorAll(".image-scroll").forEach(container => {
        container.addEventListener("wheel", (event) => {
            event.preventDefault();
            container.scrollLeft += event.deltaY;
        });
    });




document.addEventListener("click", function(event) {
    const navbarProfile = document.getElementById("navbarProfile");

    if (event.target === navbarProfile) {
        event.preventDefault(); // STOP removing navigation
    }
});


document.addEventListener("click", function(event) {
    const navbarProfile = document.getElementById("navbarProfile");

    // Ignore clicks on the navbar profile image
    if (event.target === navbarProfile) {
        event.preventDefault(); // Stop event propagation
        return;
    }

    // Handle clicks on selectable avatars
    if (event.target.matches(".nav-profile") && event.target.id !== "navbarProfile") {
        const selectedImage = event.target.src;

        fetch("/update-profile-image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_url: selectedImage })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                document.querySelector(".nav-profile").src = data.image_url; // Update navbar instantly
            }
        }).catch(error => {
            console.error("Error updating profile image:", error);
        });
    }
});




    // Ensure Submit Your Own Image button works
    const submitOwnBtn = document.getElementById("submitOwnBtn");
    const uploadBox = document.getElementById("uploadBox");

    if (submitOwnBtn && uploadBox) {
        submitOwnBtn.addEventListener("click", function() {
            uploadBox.classList.remove("hidden"); // Show upload box
            this.style.display = "none"; // Hide button
        });
    } else {
        console.error("Error: #submitOwnBtn or #uploadBox not found.");
    }

    console.log("navbar.js loaded correctly!");
});

document.getElementById("submitOwnBtn").addEventListener("click", function() {
    document.getElementById("uploadBox").classList.remove("hidden"); // Show upload box
    this.style.display = "none"; // Hide button
});

document.getElementById("fileInput").addEventListener("change", function(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("profileImage", file);

    fetch("/upload-profile-image", {
        method: "POST",
        body: formData
    }).then(response => response.json()).then(data => {
        if (data.success) {
            document.querySelector(".nav-profile").src = data.image_url; // Update navbar instantly
        } else {
            console.error("Error uploading image:", data.message);
        }
    }).catch(error => {
        console.error("Upload failed:", error);
    });
});


document.addEventListener("DOMContentLoaded", function() {
    // Set active navbar item
    function setActiveNavbar() {
        const pageName = document.title.split(" ")[1];
        const navbarItem = document.getElementById(pageName);
        if (navbarItem) {
            navbarItem.className = "active";
        }
    }
    setActiveNavbar();

    // Fetch the profile image on page load if user is logged in
    fetch("/get-profile-image", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    }).then(response => response.json()).then(data => {
        if (data.image_url) {
            document.querySelector(".nav-profile").src = data.image_url; // Update navbar profile image
        }
    }).catch(error => {
        console.error("Error fetching profile image:", error);
    });

    // Other logic for dropdowns, etc.
});








