<template>
  <div class="home container mx-auto p-8">
    <!-- Título destacado sobre la imagen -->
    <section class="welcome-message text-center py-16 mb-8">
      <h1 class="text-5xl font-bold text-white drop-shadow-md">
        Bienvenidos a <span class="text-blue-300">CEDICA</span>
      </h1>
    </section>

    <!-- Información institucional -->
    <section class="institution-info bg-white/50 p-4 mb-8 shadow border border-gray-300">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">¿Quiénes somos?</h2>
      <p class="text-gray-800 leading-relaxed text-justify">
        CEDICA es una ONG dedicada a mejorar la calidad de vida de personas con diversas condiciones físicas, mentales y emocionales a través de la equinoterapia.
        Nuestro enfoque integral combina el poder terapéutico de los caballos con un equipo de profesionales altamente capacitados para brindar un espacio seguro y de crecimiento personal.
      </p>
    </section>

    <!-- Información sobre equinoterapia -->
    <section class="equine-therapy-info bg-white/80 p-4 rounded-md shadow border border-gray-300">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">¿Qué es la Equinoterapia?</h2>
      <p class="text-gray-800 leading-relaxed text-justify">
        La equinoterapia es una terapia asistida con caballos que busca desarrollar habilidades motoras, cognitivas y emocionales en sus participantes. En CEDICA,
        nuestros caballos se convierten en compañeros esenciales en el proceso terapéutico, creando un entorno inclusivo y transformador.
      </p>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
};
</script>

<style scoped>
/* Estilo para el título sobre el fondo */
.welcome-message {
  background: none; /* Sin fondo adicional */
}

h1 {
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Sombra para destacar el texto */
}

/* Contenedores con mayor transparencia y esquinas menos redondeadas */
.institution-info,
.equine-therapy-info {
  background-color: rgba(255, 255, 255, 0.8); /* Fondo blanco más transparente */
  border-radius: 4px; /* Bordes menos redondeados */
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1); /* Sombra ligera */
}

/* Mejora en la legibilidad del texto */
p {
  line-height: 1.6; /* Espaciado entre líneas */
}
</style>
