/*Set the class of a navbar list item to "active" if the list item id is equal to the second word in <title> tag*/
function setActiveNavbar () {
    const pageName = document.title.split(' ')[1];
    const navbarItem = document.getElementById(pageName);
    if (navbarItem !== null) {
    navbarItem.className = "active";
    }
}
setActiveNavbar();