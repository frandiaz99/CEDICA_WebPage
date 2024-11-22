<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <h2 class="text-2xl font-bold text-gray-800 mb-3">{{ noticia.titulo }}</h2>
      <h4 class="text-gray-600 mb-5">Autor: {{noticia.autor}}</h4>
      <hr>
      <p class="text-blue-300 mb-1 mt-5">Creado el {{noticia.inserted_at}}</p>
      <p class="text-gray-400 mb-1">Publicado el {{noticia.fecha_publicacion}}</p>
      <p v-if="noticia.updated_at" class="text-gray-400 mb-5 italic text-sm">Actualizado el {{noticia.updated_at}}</p>
      <hr>
      <!-- Contenedor del contenido con scroll -->
      <div class="mt-4 max-h-70 overflow-y-auto">
        <p class="text-gray-800">{{ noticia.contenido }}</p>
      </div>
      
      <!-- Botón para cerrar el modal -->
      <button @click="closeModal" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Cerrar</button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['noticia'],  // Recibe la noticia que se seleccionó
  methods: {
    // Emitir el evento para cerrar el modal
    closeModal() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
/* Estilos para el modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
}

button {
  cursor: pointer;
}
</style>