import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../components/Home.vue';
import ContactoView from '../components/Contacto.vue'; 
import NoticiasView from '../components/Noticias.vue'; 
import DetalleNoticiaView from '../components/DetalleNoticia.vue';
import MainLayout from '../views/MainLayout.vue';

const routes = [
    
    { path: '/', name: 'Home', component: MainLayout},
    { path: '/home', name: 'Home', component: HomeView },
    { path: '/contacto', name: 'Contacto', component: ContactoView},
    { path: '/noticias', name: 'Noticias', component: NoticiasView },
    { path: '/noticia/:id', name: 'DetalleNoticia', component: DetalleNoticiaView },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
