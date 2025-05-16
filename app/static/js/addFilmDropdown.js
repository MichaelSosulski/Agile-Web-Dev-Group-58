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

const form = document.forms["addFilmForm"];
const clearBtn = document.getElementById("clearBtn");
function customResetForm() {
    //Clear all form fields for addFormField
    form.elements["film_title"].value = "";
    form.elements["release_year"].value = null;
    form.elements["watch_date"].value = null;
    
    const ratingRadio = form.elements["user_rating"];
    for (var i = 0; i < ratingRadio.length; i++)
        ratingRadio[i].checked = false;

    const cateRadio = form.elements["category"];
    for (var i = 0;i < cateRadio.length; i++)
        cateRadio[i].checked = false;

    form.elements["user_review"].value = "";
    form.elements["director"].value = "";
    form.elements["genres"].value = "";
    form.elements["run_time"].value = "";
    form.elements["plot"].value = "";
    form.elements["poster_url"].value = "";
}

clearBtn.addEventListener("click", customResetForm);