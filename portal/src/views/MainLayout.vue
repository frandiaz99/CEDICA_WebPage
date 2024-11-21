<template>
  <div>
    <!-- Header de navegación fijo -->
    <header class="bg-gray-800 text-white py-4 fixed w-full top-0 z-10 shadow-md">
      <div class="container mx-auto flex justify-center items-center space-x-8 px-4">
        <nav class="flex space-x-8 text-lg">
          <a href="#home" class="hover:underline transition duration-200">Inicio</a>
          <a href="#noticias" class="hover:underline transition duration-200">Noticias</a>
          <a href="#contacto" class="hover:underline transition duration-200">Contacto</a>
        </nav>
      </div>
    </header>

    <!-- Contenido principal -->
    <main class="pt-24 bg-gray-100 min-h-screen">
      <!-- Sección Home -->
      <section id="home" class="container mx-auto py-16 px-4">
        <div class="bg-white p-8 rounded-lg shadow-md">
          <Home />
        </div>
      </section>

      <!-- Sección Noticias -->
      <section id="noticias" class="container mx-auto py-16 px-4">
        <div class="bg-white p-8 rounded-lg shadow-md">
          <Noticias />
        </div>
      </section>

      <!-- Sección Contacto -->
      <section id="contacto" class="container mx-auto py-16 px-4">
        <div class="bg-white p-8 rounded-lg shadow-md">
          <Contacto />
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import Home from '@/components/Home.vue';
import Noticias from '@/components/Noticias.vue';
import Contacto from '@/components/Contacto.vue';

export default {
  components: {
    Home,
    Noticias,
    Contacto,
  },
};
</script>

<style scoped>
/* Scroll suave */
html {
  scroll-behavior: smooth;
}
</style>
