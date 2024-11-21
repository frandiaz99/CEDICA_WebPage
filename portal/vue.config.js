const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// configuracion de la api 
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Cambia el puerto según el de Flask
        changeOrigin: true
      }
    }
  }
};
