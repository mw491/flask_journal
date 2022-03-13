const body = document.body;

// Grab elements
const selectElement = (selector) => {
    const element = document.querySelector(selector);
    if(element) return element;
    throw new Error(`Something went wrong! Make sure that ${selector} exists/is typed correctly.`);  
};


// Switch theme/add to local storage
const themeToggleBtn = selectElement('#theme-toggle-btn');
const currentTheme = localStorage.getItem('currentTheme');
const navbar = selectElement("#main-nav");

// Check to see if there is a theme preference in local Storage, if so add the ligt theme to the body
if (currentTheme) {
    body.classList.add('light-theme');
    navbar.classList.remove("navbar-dark");
    navbar.classList.add("navbar-light");
} else {
    navbar.classList.remove("navbar-light");
    navbar.classList.add("navbar-dark");
}

themeToggleBtn.addEventListener('click', () => {
    // Add light theme on click
    body.classList.toggle('light-theme');
    navbar.classList.toggle("navbar-light");
    navbar.classList.toggle("navbar-dark");

    // If the body has the class of light theme then add it to local Storage, if not remove it
    if (body.classList.contains('light-theme')) {
        localStorage.setItem('currentTheme', 'themeActive');
    } else {
        localStorage.removeItem('currentTheme');
    }
});



// Search popup
searchBtn = selectElement("#search-btn");
searchContainer = selectElement("#search-container");
closeBtn = selectElement("#search-close-btn");

searchBtn.addEventListener("click", () => {
    searchContainer.classList.add("activated");
});

closeBtn.addEventListener("click", () => searchContainer.classList.remove("activated"));



var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})