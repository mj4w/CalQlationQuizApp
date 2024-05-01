document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.container');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const btnPopup = document.querySelector('.btnLogin-popup');
    const closeIcon = document.querySelector('.close-icon');
    const burgerMenu = document.querySelector('.burger-menu');
    const navList = document.querySelector('ul');
    const emailInput = document.querySelector('input[type="email"]');
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');

    // Event listener for register link click
    registerLink.addEventListener('click', function() {
        activateForm('register'); // Activate the registration form
    });

    // Event listener for login link click
    loginLink.addEventListener('click', function() {
        activateForm('login'); // Activate the login form
    });

    // Event listener for email input change
    emailInput.addEventListener('input', function() {
        resetInputStyle(emailInput); // Reset email input style
    });

    // Event listener for popup button click
    btnPopup.addEventListener('click', function() {
        openPopup(); // Open the popup
    });

    // Event listener for close icon click
    closeIcon.addEventListener('click', function() {
        closePopup(); // Close the popup
    });

    // Event listener for burger menu click
    burgerMenu.addEventListener('click', function() {
        toggleMenu(); // Toggle the navigation menu visibility
    });

    // Event listener for toggling password visibility (login form)
    togglePasswordIcons.forEach(function(icon) {
        icon.addEventListener('click', function() {
            togglePasswordVisibility(icon);
        });
    });

    // Function to activate login or registration form
    function activateForm(formType) {
        if (formType === 'register') {
            container.classList.add('active');
        } else if (formType === 'login') {
            container.classList.remove('active');
        }
        closeIcon.style.display = 'block'; // Display close icon for forms
    }

    // Function to open the popup
    function openPopup() {
        container.classList.add('active-popup');
        closeIcon.style.display = 'block'; // Display close icon when popup is opened
    }

    // Function to close the popup
    function closePopup() {
        container.classList.remove('active-popup');
        burgerMenu.classList.remove('active');
        navList.classList.remove('active');
        closeIcon.style.display = 'none'; // Hide close icon when popup is closed
    }

    // Function to toggle the navigation menu visibility
    function toggleMenu() {
        navList.classList.toggle('active');
        burgerMenu.classList.toggle('active');
        closeIcon.style.display = 'block'; // Display close icon when burger menu is clicked
    }

    // Function to toggle password visibility
    function togglePasswordVisibility(icon) {
        const passwordInput = icon.previousElementSibling; // Get the password input field
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    }
});
