<template>
  <nav class="bg-blue-500 p-4" aria-label="Navegación principal">
    <div class="container mx-auto">
      <!-- Botón de menú móvil -->
      <div class="flex items-center justify-between md:hidden">
        <router-link to="/" class="text-white font-bold">Club Esportiu Garraf</router-link>
        <button @click="toggleMenu" class="text-white focus:outline-none ml-4">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Menú de escritorio -->
      <div class="hidden md:flex md:justify-between md:items-center">
        <div class="flex items-center">
          <router-link to="/" class="text-white font-bold text-xl">Club Esportiu Garraf</router-link>
        </div>

        <div class="flex items-center space-x-6 ml-auto">
          <div v-if="isAuthenticated && isAdmin" class="flex items-center space-x-6">
            <router-link to="/reservar" class="text-white hover:text-gray-200">Reservar</router-link>
            <router-link to="/administradores" class="text-white hover:text-gray-200">Administradores</router-link>
            <router-link to="/socios" class="text-white hover:text-gray-200">Socios</router-link>
            <router-link to="/pistas" class="text-white hover:text-gray-200">Pistas</router-link>
          </div>

          <div v-if="isAuthenticated && isSocio" class="flex items-center space-x-6">
            <router-link to="/reservar" class="text-white hover:text-gray-200">Reservar</router-link>
            <router-link to="/mis-reservas" class="text-white hover:text-gray-200">Mis Reservas</router-link>
            <router-link to="/mi-perfil" class="text-white hover:text-gray-200">Mi Perfil</router-link>
          </div>

          <div class="flex items-center">
            <template v-if="!isAuthenticated">
              <router-link to="/login" class="text-white hover:text-gray-200">Login</router-link>
            </template>
            <template v-else>
              <a @click="handleLogout" class="text-white hover:text-gray-200 cursor-pointer">Logout</a>
            </template>
          </div>
        </div>
      </div>

      <!-- Menú móvil -->
      <div v-show="isMenuOpen" class="md:hidden mt-4">
        <div class="flex flex-col space-y-3">
          <template v-if="isAuthenticated && isAdmin">
            <router-link to="/reservar" class="text-white py-2" @click="closeMenu">Reservar</router-link>
            <router-link to="/administradores" class="text-white py-2" @click="closeMenu">Administradores</router-link>
            <router-link to="/socios" class="text-white py-2" @click="closeMenu">Socios</router-link>
            <router-link to="/pistas" class="text-white py-2" @click="closeMenu">Pistas</router-link>
          </template>

          <template v-if="isAuthenticated && isSocio">
            <router-link to="/reservar" class="text-white py-2" @click="closeMenu">Reservar</router-link>
            <router-link to="/mis-reservas" class="text-white py-2" @click="closeMenu">Mis Reservas</router-link>
            <router-link to="/mi-perfil" class="text-white py-2" @click="closeMenu">Mi Perfil</router-link>
          </template>

          <template v-if="!isAuthenticated">
            <router-link to="/login" class="text-white py-2" @click="closeMenu">Login</router-link>
          </template>
          <template v-else>
            <a @click="handleLogoutAndClose" class="text-white py-2 cursor-pointer">Logout</a>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    },
    isAdmin: {
      type: Boolean,
      required: true
    },
    isSocio: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      isMenuOpen: false
    }
  },
  emits: ['logout'],
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen
    },
    closeMenu() {
      this.isMenuOpen = false
    },
    handleLogout() {
      // Limpiar todas las credenciales
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      sessionStorage.removeItem('token');
      sessionStorage.removeItem('userRole');
      
      // Forzar recarga de la página para limpiar el estado
      window.location.href = '/';
    },
    handleLogoutAndClose() {
      this.closeMenu();
      this.handleLogout();
    }
  },
  watch: {
    '$route'() {
      this.isMenuOpen = false
    }
  }
}
</script>

<style scoped>
.router-link-active {
  font-weight: bold;
  text-decoration: underline;
}
</style>