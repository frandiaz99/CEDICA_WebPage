// script.js

document.addEventListener('DOMContentLoaded', function() {
    const infoBtn = document.getElementById('infoBtn');
    const docsBtn = document.getElementById('docsBtn');
    const infoSection = document.getElementById('infoSection');
    const docsSection = document.getElementById('docsSection');

    // Función para mostrar la sección de información general y ocultar la de documentos
    infoBtn.addEventListener('click', function() {
        infoSection.classList.remove('hidden');
        docsSection.classList.add('hidden');
        actionButtons.style.display = 'flex';
        infoBtn.classList.add('bg-blue-500', 'text-white');
        infoBtn.classList.remove('bg-gray-200', 'text-gray-700');
        docsBtn.classList.add('bg-gray-200', 'text-gray-700');
        docsBtn.classList.remove('bg-blue-500', 'text-white');
    });

    // Función para mostrar la sección de documentos y ocultar la de información general
    docsBtn.addEventListener('click', function() {
        docsSection.classList.remove('hidden');
        infoSection.classList.add('hidden');
        actionButtons.style.display = 'none';
        docsBtn.classList.add('bg-blue-500', 'text-white');
        docsBtn.classList.remove('bg-gray-200', 'text-gray-700');
        infoBtn.classList.add('bg-gray-200', 'text-gray-700');
        infoBtn.classList.remove('bg-blue-500', 'text-white');
    });
});
