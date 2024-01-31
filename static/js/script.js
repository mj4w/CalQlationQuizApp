document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.container');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const btnPopup = document.querySelector('.btnLogin-popup');
    const closeIcon = document.querySelector('.close-icon');
    const burgerMenu = document.querySelector('.burger-menu');
    const navList = document.querySelector('ul');

    registerLink.addEventListener('click', () => {
        container.classList.add('active');
        closeIcon.style.display = 'block'; // Display close icon when the registration form is active
    });

    loginLink.addEventListener('click', () => {
        container.classList.remove('active');
        closeIcon.style.display = 'block'; // Display close icon when the login form is active
    });

    btnPopup.addEventListener('click', () => {
        container.classList.add('active-popup');
        closeIcon.style.display = 'block'; // Display close icon when popup is opened
    });

    closeIcon.addEventListener('click', () => {
        container.classList.remove('active-popup');
        burgerMenu.classList.remove('active');
        navList.classList.remove('active');
        closeIcon.style.display = 'none'; // Hide close icon when popup is closed
    });

    burgerMenu.addEventListener('click', () => {
        navList.classList.toggle('active');
        burgerMenu.classList.toggle('active');
        closeIcon.style.display = 'block'; // Display close icon when burger menu is clicked
    });
});