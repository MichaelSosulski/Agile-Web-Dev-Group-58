function toggleVisible(dropdownId) {
    document.getElementById(dropdownId).classList.toggle("show");
}
document.getElementById("loginBtn").addEventListener("click", function() {toggleVisible("loginDropdown"); });
document.getElementById("signupBtn").addEventListener("click", function() {toggleVisible("signupDropdown"); });