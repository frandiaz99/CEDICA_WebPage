// navbar.js

document.addEventListener("DOMContentLoaded", function () {
    // Manejo del menú móvil
    const mobileMenuButton = document.querySelector("button[aria-controls='mobile-menu']");
    const mobileMenu = document.getElementById("mobile-menu");

    mobileMenuButton.addEventListener("click", function () {
        const isOpen = mobileMenuButton.getAttribute("aria-expanded") === "true";
        mobileMenuButton.setAttribute("aria-expanded", !isOpen);
        mobileMenu.classList.toggle("hidden");
    });

    // Manejo del menú desplegable de usuario
    const userMenuButton = document.getElementById("user-menu-button");
    const userMenu = userMenuButton.nextElementSibling; // El menú desplegable

    userMenuButton.addEventListener("click", function () {
        const isOpen = userMenuButton.getAttribute("aria-expanded") === "true";
        userMenuButton.setAttribute("aria-expanded", !isOpen);
        userMenu.classList.toggle("hidden");
    });

    // Cerrar el menú desplegable al hacer clic fuera de él
    window.addEventListener("click", function (event) {
        if (!userMenuButton.contains(event.target) && !userMenu.contains(event.target)) {
            userMenu.classList.add("hidden");
            userMenuButton.setAttribute("aria-expanded", "false");
        }
    });

    // Cerrar el menú móvil al hacer clic en un enlace
    const mobileMenuLinks = mobileMenu.querySelectorAll("a");
    mobileMenuLinks.forEach(link => {
        link.addEventListener("click", function () {
            mobileMenu.classList.add("hidden");
            mobileMenuButton.setAttribute("aria-expanded", "false");
        });
    });
});

