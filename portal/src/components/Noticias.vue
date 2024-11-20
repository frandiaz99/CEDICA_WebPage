<template>
  <div class="noticias container mx-auto p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Noticias</h2>
    <ul>
      <li v-for="noticia in noticias" :key="noticia.id" class="bg-gray-100 p-6 rounded-lg mb-4 shadow-md">

        <p class="text-xl font-semibold text-gray-800 w-full text-center">{{ noticia.titulo }}</p>
        <p class="text-gray-500 text-sm">Subido por: {{ noticia.autor }}</p>
        <p class="text-gray-400 text-sm">{{ noticia.fecha_publicacion }}</p>
        <p class="text-gray-700">{{ noticia.copete }}</p>

        <a href="">Ver noticia completa</a>

      </li>
    </ul>
    <p v-if="!noticias.length">No hay noticias nuevas.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NoticiasView',
  data() {
    return {
      noticias: [],
      error: null, // Para manejar posibles errores
    };
  },
  async created() {
    try {
      // Hacer la solicitud GET usando async/await
      const response = await axios.get('http://127.0.0.1:5000/api/publicaciones');
      this.noticias = response.data.map(noticia => ({
        ...noticia,
      }));
    } catch (error) {
      console.error('Hubo un error al cargar las noticias:', error);
      this.error = 'Hubo un problema al cargar las noticias.';
    }
  },
};
</script>