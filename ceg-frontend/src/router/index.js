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
import axios from 'axios'

const routes = [
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: false } },
  { path: '/login', name: 'Login', component: Login, meta: { requiresAuth: false } },
  { path: '/register', name: 'Register', component: Register, meta: { requiresAuth: false } },
  {
    path: '/reservar/:id?',
    name: 'Reservar',
    component: Reservas,
    props: true,
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
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/mis-reservas/editar/:id',
    name: 'EditarMiReserva',
    component: Reservas,
    meta: { requiresAuth: true, requiresSocio: true }
  },
  { 
    path: '/reservar', 
    name: 'Reservar', 
    component: Reservas, 
    meta: { requiresAuth: true }
  },
  { 
    path: '/mis-reservas', 
    name: 'MisReservas', 
    component: MisReservas, 
    meta: { requiresAuth: true, requiresSocio: true }
  },
  {
    path: '/mi-perfil',
    name: 'MiPerfil',
    component: MiPerfil,
    meta: { requiresAuth: true, requiresSocio: true }
  },
  { path: '/logout', name: 'Logout', component: Logout, meta: { requiresAuth: false } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: Home }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Funciones de ayuda para el almacenamiento
const storage = {
  getItem(key) {
    try {
      return localStorage.getItem(key) || sessionStorage.getItem(key);
    } catch (e) {
      console.error('Error accediendo al almacenamiento:', e);
      return null;
    }
  },
  
  setItem(key, value) {
    try {
      localStorage.setItem(key, value);
      sessionStorage.setItem(key, value);
    } catch (e) {
      console.error('Error guardando en almacenamiento:', e);
      try {
        sessionStorage.setItem(key, value);
      } catch (e2) {
        console.error('Error guardando en sessionStorage:', e2);
      }
    }
  },
  
  removeItem(key) {
    try {
      localStorage.removeItem(key);
      sessionStorage.removeItem(key);
    } catch (e) {
      console.error('Error eliminando del almacenamiento:', e);
    }
  }
};

// Función para verificar el token con el backend
async function verifyToken(token, userRole) {
  try {
    console.log('Verificando token para rol:', userRole);
    const url = userRole === 'admin' 
      ? 'http://192.168.10.21:8000/admin/me'
      : 'http://192.168.10.21:8000/socios/me';
    
    console.log('Haciendo petición a:', url);
    const response = await axios.get(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    console.log('Respuesta de verificación:', response.data);
    return true;
  } catch (error) {
    console.error('Error verificando token:', error);
    if (error.response) {
      console.error('Respuesta del servidor:', error.response.data);
      console.error('Estado:', error.response.status);
    }
    return false;
  }
}

router.beforeEach(async (to, from, next) => {
  console.log('Navegando a:', to.path);
  const token = storage.getItem('token');
  const userRole = storage.getItem('userRole');
  const isPublicRoute = to.meta.requiresAuth === false;

  console.log('Token:', token ? 'Presente' : 'Ausente');
  console.log('Rol:', userRole);
  console.log('Ruta pública:', isPublicRoute);

  // Si es una ruta pública, permitir acceso
  if (isPublicRoute) {
    console.log('Permitiendo acceso a ruta pública');
    return next();
  }

  // Si no hay token y la ruta requiere autenticación
  if (!token && to.meta.requiresAuth) {
    console.log('No hay token, redirigiendo a login');
    return next('/login');
  }

  // Si hay token, verificar su validez
  if (token) {
    console.log('Verificando validez del token');
    const isValidToken = await verifyToken(token, userRole);
    
    if (!isValidToken) {
      console.log('Token inválido, limpiando almacenamiento');
      storage.removeItem('token');
      storage.removeItem('userRole');
      return next('/login');
    }

    // Verificar permisos específicos
    if (to.meta.requiresAdmin && userRole !== 'admin') {
      console.log('Acceso denegado: se requiere ser admin');
      return next('/');
    }

    if (to.meta.requiresSocio && userRole !== 'socio') {
      console.log('Acceso denegado: se requiere ser socio');
      return next('/');
    }

    // Si todo está bien, permitir acceso
    console.log('Acceso permitido');
    return next();
  }

  // Si llegamos aquí, algo salió mal
  console.log('Error inesperado, redirigiendo a login');
  next('/login');
});

export default router