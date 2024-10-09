document.addEventListener('DOMContentLoaded', function() {
    const infoBtn = document.getElementById('infoBtn');
    const docsBtn = document.getElementById('docsBtn');
    const infoSection = document.getElementById('infoSection');
    const docsSection = document.getElementById('docsSection');

    // Función para mostrar la sección de información general y ocultar la de documentos
    infoBtn.addEventListener('click', function() {
        showInfoSection();
        localStorage.setItem('activeTab', 'info'); // Guardar el estado en localStorage
    });

    // Función para mostrar la sección de documentos y ocultar la de información general
    docsBtn.addEventListener('click', function() {
        showDocsSection();
        localStorage.setItem('activeTab', 'docs'); // Guardar el estado en localStorage
    });

    // Función para mostrar la sección de información
    function showInfoSection() {
        infoSection.classList.remove('hidden');
        docsSection.classList.add('hidden');
        
        infoBtn.classList.add('bg-blue-500', 'text-white');
        infoBtn.classList.remove('bg-gray-200', 'text-gray-700');
        docsBtn.classList.add('bg-gray-200', 'text-gray-700');
        docsBtn.classList.remove('bg-blue-500', 'text-white');
    }

    // Función para mostrar la sección de documentos
    function showDocsSection() {
        docsSection.classList.remove('hidden');
        infoSection.classList.add('hidden');
        
        docsBtn.classList.add('bg-blue-500', 'text-white');
        docsBtn.classList.remove('bg-gray-200', 'text-gray-700');
        infoBtn.classList.add('bg-gray-200', 'text-gray-700');
        infoBtn.classList.remove('bg-blue-500', 'text-white');
    }

    // Comprobar qué pestaña estaba activa antes de recargar la página usando localStorage
    const activeTab = localStorage.getItem('activeTab');

    if (activeTab === 'docs') {
        showDocsSection();
    } else {
        showInfoSection();  // Por defecto se muestra la sección de información
    }
});
