<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function () {
    // 1. Set active navbar item
    function setActiveNavbar() {
        const pageName = document.title.split(" ")[1];
        const navbarItem = document.getElementById(pageName);
        if (navbarItem) {
            navbarItem.classList.add("active");  // Use classList.add() to safely add 'active'
        }
    }
    setActiveNavbar();

    // 2. Dropdown handling
    function toggleVisible(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            document.querySelectorAll(".dropdown-content").forEach(container => {
                container.style.display = container.id !== dropdownId
                    ? "none"
                    : container.style.display === "block" ? "none" : "block";
            });
        }
    }

    // Close dropdowns if click is outside
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

    // 3. Login and signup buttons
    const loginBtn = document.getElementById("loginBtn");
    const signupBtn = document.getElementById("signupBtn");

    if (loginBtn) {
        loginBtn.addEventListener("click", function () {
            toggleVisible("loginDropdown");
        });
    }

    if (signupBtn) {
        signupBtn.addEventListener("click", function () {
            toggleVisible("signupDropdown");
        });
    }

    // 4. Enable horizontal scrolling for image containers
    document.querySelectorAll(".image-scroll").forEach(container => {
        container.addEventListener("wheel", (event) => {
            event.preventDefault();
            container.scrollLeft += event.deltaY;
        });
    });

    // 5. Fetch and show saved profile image on page load
    fetch("/get-profile-image", {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        if (data.image_url) {
            const navbarImg = document.getElementById("navbarProfile");
            if (navbarImg) {
                navbarImg.src = data.image_url;
            }
        }
    })
    .catch(error => {
        console.error("Error fetching profile image:", error);
    });

    // 6. Handle avatar selection clicks
    document.addEventListener("click", function (event) {
        const clickedImage = event.target;

        if (
            clickedImage.classList.contains("nav-profile") &&
            clickedImage.id !== "navbarProfile"
        ) {
            const selectedImage = clickedImage.src;

            fetch("/update-profile-image", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ image_url: selectedImage })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const navbarProfile = document.getElementById("navbarProfile");
                    if (navbarProfile) {
                        navbarProfile.src = data.image_url;
                    }
                }
            })
            .catch(error => {
                console.error("Error updating profile image:", error);
            });
        }
    });

    // 7. Handle custom image upload
    const fileInput = document.getElementById("fileInput");
    if (fileInput) {
        fileInput.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append("profileImage", file);

            fetch("/upload-profile-image", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    const navbarImg = document.getElementById("navbarProfile");
                    if (navbarImg) {
                        navbarImg.src = data.image_url;
                    }
                } else {
                    console.error("Error uploading image:", data.message);
                }
            })
            .catch(error => {
                console.error("Upload failed:", error);
            });
        });
    }

    // 8. Show custom image upload box
    const submitOwnBtn = document.getElementById("submitOwnBtn");
    const uploadBox = document.getElementById("uploadBox");

    if (submitOwnBtn && uploadBox) {
        submitOwnBtn.addEventListener("click", function () {
            uploadBox.classList.remove("hidden");
            this.style.display = "none";
        });
    }

    console.log("navbar.js loaded correctly!");


    document.querySelectorAll('.nav-profile').forEach(function(img) {
        img.addEventListener('click', function() {
            const selectedAvatar = img.getAttribute('data-avatar');
            const profileImage = document.querySelector('.user-profile img');  // Assuming this is where you show the user's profile image
            profileImage.src = "{{ url_for('static', filename='') }}" + selectedAvatar;

            // You can also send the selected avatar to your server and update the user's profile in the database
            fetch('/update-avatar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ avatar: selectedAvatar }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Avatar updated successfully!");
                } else {
                    console.error("Error updating avatar");
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});










=======
/*Set the class of a navbar list item to "active" if the list item id is equal to the second word in <title> tag*/
function setActiveNavbar () {
    const pageName = document.title.split(' ')[1];
    const navbarItem = document.getElementById(pageName);
    if (navbarItem !== null) {
    navbarItem.className = "active";
    }
}
setActiveNavbar();
>>>>>>> main
