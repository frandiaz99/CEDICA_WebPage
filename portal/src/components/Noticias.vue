<template>
  <div class="noticias container mx-auto p-8">
    <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Noticias</h2>
    <ul>
      <li v-for="noticia in noticiasPublicadas" :key="noticia.id" class="bg-gray-100 p-6 rounded-lg mb-4 shadow-md">
        <p class="text-xl font-semibold text-gray-800 w-full text-center">{{ noticia.titulo }}</p>
        <p class="text-gray-400 text-sm">{{ noticia.fecha_publicacion }}</p>
        <p class="text-gray-700">{{ noticia.copete }}</p>

        <!-- Botón para abrir el modal -->
        <button @click="openModal(noticia)" class="text-blue-500">Ver noticia completa</button>
      </li>
    </ul>
    
    <!-- Mostrar un mensaje si no hay noticias -->
    <p v-if="!noticias.length">No hay noticias nuevas.</p>

    <!-- Modal de detalles de la noticia -->
    <DetalleNoticia
      v-if="isModalOpen"
      :noticia="selectedNoticia"
      @close="closeModal"
    />
  </div>
</template>

<script>
import axios from 'axios';
import DetalleNoticia from './DetalleNoticia.vue';  // Importamos el componente modal

export default {
  components: {
    DetalleNoticia
  },
  data() {
    return {
      noticias: [],
      error: null, 
      isModalOpen: false,  // Estado para controlar si el modal está abierto o cerrado
      selectedNoticia: null,  // La noticia seleccionada para mostrar en el modal
    };
  },
  async created() {
    try {
      // Hacer la solicitud GET usando async/await
      const response = await axios.get('http://127.0.0.1:5000/api/publicaciones');
      this.noticias = response.data;
    } catch (error) {
      console.error('Hubo un error al cargar las noticias:', error);
      this.error = 'Hubo un problema al cargar las noticias.';
    }
  },
  computed: {
    // Filtrar solo las noticias publicadas
    noticiasPublicadas() {
      return this.noticias.filter(noticia => noticia.estado === 'publicado');
    }
  },
  methods: {
    // Abrir el modal y pasar la noticia seleccionada
    openModal(noticia) {
      this.selectedNoticia = noticia;
      this.isModalOpen = true;
    },
    // Cerrar el modal
    closeModal() {
      this.isModalOpen = false;
      this.selectedNoticia = null;
    }
  }
};
</script>

<style scoped>
/* Aquí puedes agregar los estilos para el modal si lo necesitas */
</style>