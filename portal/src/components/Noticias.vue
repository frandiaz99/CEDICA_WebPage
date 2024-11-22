<template>
  <div class="noticias container mx-auto p-8">
    <h1 class="text-2xl font-bold text-center text-gray-800 mb-6">Noticias</h1>
    
    <!-- Grilla de noticias -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="noticia in noticiasPaginadas"
        :key="noticia.id"
        class="bg-gray-100 p-6 shadow-md"
      >
        <p class="text-xl font-semibold text-gray-800 w-full text-center">{{ noticia.titulo }}</p>
        <p class="text-gray-400 text-sm text-center">{{ noticia.fecha_publicacion }}</p>
        <p class="text-gray-700 text-center">{{ noticia.copete }}</p>
        
        <!-- Botón para abrir el modal -->
        <div class="text-center mt-4">
          <button
            @click="openModal(noticia)"
            class="text-blue-500 underline"
          >
            Ver noticia completa
          </button>
        </div>
      </div>
    </div>

    <!-- Mostrar un mensaje si no hay noticias -->
    <p v-if="!noticiasPublicadas.length" class="text-center mt-8">No hay noticias nuevas.</p>

    <!-- Paginación -->
    <div class="flex justify-center items-center mt-8 space-x-4">
      <button
        @click="paginaActual--"
        :disabled="paginaActual === 1"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >
        Anterior
      </button>
      <span>Página {{ paginaActual }} de {{ totalPaginas }}</span>
      <button
        @click="paginaActual++"
        :disabled="paginaActual === totalPaginas"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
      >
        Siguiente
      </button>
    </div>

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
import DetalleNoticia from './DetalleNoticia.vue'; // Importamos el componente modal

export default {
  components: {
    DetalleNoticia
  },
  data() {
    return {
      noticias: [],
      error: null,
      isModalOpen: false,
      selectedNoticia: null,
      paginaActual: 1, // Página actual
      noticiasPorPagina: 4 // Cambiamos a 6 noticias por página
    };
  },
  async created() {
    try {
      const response = await axios.get('https://admin-grupo49.proyecto2024.linti.unlp.edu.ar/api/publicaciones/');
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
    },
    // Calcular las noticias a mostrar en la página actual
    noticiasPaginadas() {
      const inicio = (this.paginaActual - 1) * this.noticiasPorPagina;
      const fin = inicio + this.noticiasPorPagina;
      return this.noticiasPublicadas.slice(inicio, fin);
    },
    // Calcular el número total de páginas
    totalPaginas() {
      return Math.ceil(this.noticiasPublicadas.length / this.noticiasPorPagina);
    }
  },
  methods: {
    openModal(noticia) {
      this.selectedNoticia = noticia;
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
      this.selectedNoticia = null;
    }
  }
};
</script>
