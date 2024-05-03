let slideIndex = 1;

function showSlides(n) {
    const slides = document.querySelector(".team-slider");
    const dots = document.querySelectorAll(".dot");

    if (n > slides.children.length) {
        slideIndex = 1;
    }

    if (n < 1) {
        slideIndex = slides.children.length;
    }

    for (let i = 0; i < slides.children.length; i++) {
        slides.children[i].style.display = "none";
    }

    for (let i = 0; i < dots.length; i++) {
        dots[i].classList.remove("active");
    }

    slides.children[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].classList.add("active");
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

// Initial setup
showSlides(slideIndex);