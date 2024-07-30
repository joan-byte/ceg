import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Reservas from '../views/Reservas.vue'
import Administradores from '../views/Administradores.vue'
import Socios from '../views/Socios.vue'
import Pistas from '../views/Pistas.vue'
import MisReservas from '../views/MisReservas.vue'
import Logout from '../views/Logout.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/reservas', name: 'Reservas', component: Reservas },
  { path: '/administradores', name: 'Administradores', component: Administradores },
  { path: '/socios', name: 'Socios', component: Socios },
  { path: '/pistas', name: 'Pistas', component: Pistas },
  { path: '/mis-reservas', name: 'MisReservas', component: MisReservas },
  { path: '/reservar', name: 'Reservar', component: Reservas },
  { path: '/logout', name: 'Logout', component: Logout }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router