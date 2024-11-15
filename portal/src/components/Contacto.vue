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
        <input type="email" id="email" v-model="email" required
          class="w-full p-2 border border-gray-300 rounded mt-1" />
      </div>
      <div class="mb-4">
        <label for="message" class="block text-gray-700">Mensaje</label>
        <textarea id="message" v-model="message" required
          class="w-full p-2 border border-gray-300 rounded mt-1"></textarea>
      </div>
      <div class="g-recaptcha mb-4" data-sitekey="6LfWlX8qAAAAAPBA1xt4Lyqci8obXzNhMqziWybq"></div>
      <button type="submit" class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Enviar</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ContactoView',
  data() {
    return {
      name: '',
      email: '',
      message: '',
      recaptchaSiteKey: '6LfWlX8qAAAAAPBA1xt4Lyqci8obXzNhMqziWybq',
      recaptchaLoaded: false,
    };
  },
  methods: {
    async submitForm() {
      //eslint-disable-next-line no-undef 
      const recaptchaResponse = grecaptcha.getResponse();
      if (!recaptchaResponse) {
        alert('Please complete the CAPTCHA');
        return;
      }

      const formData = {
        nombre_completo: this.name,
        correo_electronico: this.email,
        mensaje: this.message,
        recaptchaResponse: recaptchaResponse,
      };

      try {
        const response = await axios.post('/api/contacto', formData);
        if (response.data.success) {
          alert('Message sent successfully');
        } else {
          alert('CAPTCHA validation failed');
        }
      } catch (error) {
        alert('Error sending message');
      }
    }


  },
  mounted() {
    const script = document.createElement('script');
    script.src = 'https://www.google.com/recaptcha/api.js';
    script.async = true;
    script.onload = () => {
      this.recaptchaLoaded = true;
    };
    document.head.appendChild(script);
  },
};
</script>
