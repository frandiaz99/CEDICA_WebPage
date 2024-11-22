<template>
  <div>
    <!-- Header de navegación fijo -->
    <header class="bg-gray-800 text-white py-4 fixed w-full top-0 z-10 shadow-md">
  <div class="container mx-auto flex justify-center items-center px-4">
    <nav class="flex space-x-8 text-lg font-semibold tracking-wide uppercase">
      <a 
        href="#home" 
        class="hover:text-yellow-400 transition duration-300 transform hover:scale-105">
        Inicio
      </a>
      <a 
        href="#noticias" 
        class="hover:text-yellow-400 transition duration-300 transform hover:scale-105">
        Noticias
      </a>
      <a 
        href="#contacto" 
        class="hover:text-yellow-400 transition duration-300 transform hover:scale-105">
        Contacto
      </a>
    </nav>
  </div>
</header>


    <!-- Contenido principal -->
    <main class="pt-24 bg-overlay min-h-screen">
      <!-- Sección Home -->
      <section id="home" class="container mx-auto py-16 px-4">
        <div class="p-8 rounded-lg">
          <Home />
        </div>
      </section>

      <!-- Sección Noticias -->
      <section id="noticias" class="container mx-auto py-16 px-4">
        <div class="bg-news-contact p-8 shadow-lg">
          <Noticias />
        </div>
      </section>

      <!-- Sección Contacto -->
      <section id="contacto" class="container mx-auto py-16 px-4">
        <div class="bg-news-contact p-8 shadow-lg">
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

.bg-overlay {
  background-image: url('https://images.pexels.com/photos/265216/pexels-photo-265216.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}


.bg-news-contact {
  background-color: rgba(255, 255, 255, 0.); 
  backdrop-filter: blur(4px); 
  border: 1px solid rgba(0, 0, 0, 0.1); 
}


html {
  scroll-behavior: smooth;
}


.shadow-lg {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
}

.rounded-lg {
  border-radius: 12px;
}


header {
  background: linear-gradient(90deg, #2c3e50, #34495e); 
}


nav a {
  font-family: 'Poppins', sans-serif; 
  letter-spacing: 0.05em; 
  text-transform: uppercase; 
  color: #f8f9fa;
}


nav a:hover {
  color: grey; 
}


nav a {
  transition: color 0.3s ease, transform 0.3s ease;
}
</style>
