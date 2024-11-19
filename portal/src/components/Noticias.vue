<template>
    <div class="noticias container mx-auto p-8">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Noticias</h2>
      <ul>
        <li v-for="noticia in noticias" :key="noticia.id" class="bg-gray-100 p-6 rounded-lg mb-4 shadow-md">
          <h3 class="text-xl font-semibold text-gray-800">{{ noticia.titulo }}</h3>
          <p class="text-gray-500 text-sm">{{ noticia.fechaPublicacion }}</p>
          <p class="text-gray-700">{{ noticia.copete }}</p>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NoticiasView',
    data() {
      return {
        noticias: [
          { id: 1, titulo: "Noticia 1", fechaPublicacion: "2023-10-01", copete: "Resumen de la noticia 1" },
          { id: 2, titulo: "Noticia 2", fechaPublicacion: "2023-09-20", copete: "Resumen de la noticia 2" },
        ],
      };
    },
    created() {
      // Cargar noticias desde la API aquí
      
    },
  };
  </script>
  