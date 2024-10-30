<template>
    <div class="contact container mx-auto p-8">
      <h2 class="text-2xl font-bold text-center text-gray-800 mb-6">Contacto</h2>
      <form @submit.prevent="submitForm" class="bg-gray-100 p-6 rounded-lg shadow-md max-w-md mx-auto">
        <div class="mb-4">
          <label for="name" class="block text-gray-700">Nombre completo</label>
          <input type="text" id="name" v-model="name" required class="w-full p-2 border border-gray-300 rounded mt-1" />
        </div>
        <div class="mb-4">
          <label for="email" class="block text-gray-700">Correo electrónico</label>
          <input type="email" id="email" v-model="email" required class="w-full p-2 border border-gray-300 rounded mt-1" />
          <span v-if="emailError" class="text-red-500 text-sm">Ingrese un correo válido</span>
        </div>
        <div class="mb-4">
          <label for="message" class="block text-gray-700">Mensaje</label>
          <textarea id="message" v-model="message" required class="w-full p-2 border border-gray-300 rounded mt-1"></textarea>
        </div>
        <div class="mb-4">
          <label for="captcha" class="block text-gray-700">Captcha</label>
          <input type="text" id="captcha" v-model="captcha" required class="w-full p-2 border border-gray-300 rounded mt-1" />
        </div>
        <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Enviar</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ContactoView',
    data() {
      return {
        name: '',
        email: '',
        message: '',
        captcha: '',
        emailError: false,
      };
    },
    methods: {
      validateEmail() {
        const regex = /\S+@\S+\.\S+/;
        this.emailError = !regex.test(this.email);
      },
      submitForm() {
        this.validateEmail();
        if (!this.emailError && this.name && this.message && this.captcha) {
          // Llama al endpoint de la API para enviar el mensaje
        } else {
          alert('Por favor completa todos los campos correctamente.');
        }
      },
    },
  };
  </script>
  