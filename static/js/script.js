const container = document.querySelector('.container');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');

registerLink.addEventListener('click', ()=> {
    container.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    container.classList.remove('active');
});

const btnPopup = document.querySelector('.btnLogin-popup');

btnPopup.addEventListener('click', ()=> {
    container.classList.add('active-popup');
});

const closeIcon = document.querySelector('.close-icon');

closeIcon.addEventListener('click', ()=> {
    container.classList.remove('active-popup');
});
