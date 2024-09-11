import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Reservas from '../views/Reservas.vue'
import Administradores from '../views/Administradores.vue'
import Socios from '../views/Socios.vue'
import Pistas from '../views/Pistas.vue'
import MisReservas from '../views/MisReservas.vue'
import MiPerfil from '../views/MiPerfil.vue'
import Logout from '../views/Logout.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { 
    path: '/reservas', 
    name: 'Reservas', 
    component: Reservas, 
    meta: { requiresAuth: true }
  },
  {
    path: '/reservas/:id/edit',
    name: 'EditarReserva',
    component: Reservas,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { 
    path: '/administradores', 
    name: 'Administradores', 
    component: Administradores, 
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { 
    path: '/socios', 
    name: 'Socios', 
    component: Socios, 
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { 
    path: '/pistas', 
    name: 'Pistas', 
    component: Pistas, 
    meta: { requiresAuth: true }
  },
  { 
    path: '/mis-reservas', 
    name: 'MisReservas', 
    component: MisReservas, 
    meta: { requiresAuth: true, requiresSocio: true }
  },
  { 
    path: '/reservar', 
    name: 'Reservar', 
    component: Reservas, 
    meta: { requiresAuth: true }
  },
  {
    path: '/mi-perfil',
    name: 'MiPerfil',
    component: MiPerfil,
    meta: { requiresAuth: true }
  },
  { path: '/logout', name: 'Logout', component: Logout },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: Home }  // Ruta catch-all
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token') !== null
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && userRole !== 'admin') {
    next('/')  // Redirigir a la página principal si no es admin
  } else {
    next()
  }
})

export default router