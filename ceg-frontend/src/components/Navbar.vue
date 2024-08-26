<template>
  <nav class="bg-blue-500 p-4" aria-label="Navegación principal">
    <ul class="flex space-x-4">
      <li><router-link to="/" class="text-white">Reservas</router-link></li>
      <li v-if="!isAuthenticated"><router-link to="/register" class="text-white">Register</router-link></li>
      <li v-if="!isAuthenticated"><router-link to="/login" class="text-white">Login</router-link></li>
      <li v-if="isAuthenticated"><a @click="handleLogout" class="text-white cursor-pointer">Logout</a></li>

      <template v-if="isAdmin">
        <li><router-link to="/administradores" class="text-white">Administradores</router-link></li>
        <li><router-link to="/socios" class="text-white">Socios</router-link></li>
        <li><router-link to="/pistas" class="text-white">Pistas</router-link></li>
        <li><router-link to="/reservar" class="text-white">Reservar</router-link></li>
      </template>

      <template v-if="isSocio">
        <li><router-link to="/mis-reservas" class="text-white">Mis Reservas</router-link></li>
        <li><router-link to="/reservar" class="text-white">Reservar</router-link></li>
      </template>
    </ul>
  </nav>
  <div v-if="showDebug" class="debug-info">
    <p>Autenticado: {{ isAuthenticated }}</p>
    <p>Admin: {{ isAdmin }}</p>
    <p>Socio: {{ isSocio }}</p>
  </div>
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
  emits: ['logout'],
  data() {
    return {
      showDebug: process.env.NODE_ENV === 'development'
    }
  },
  methods: {
    handleLogout() {
      this.$emit('logout');
    }
  },
  watch: {
    isAuthenticated(newVal) {
      console.log('isAuthenticated changed:', newVal);
    },
    isAdmin(newVal) {
      console.log('isAdmin changed:', newVal);
    },
    isSocio(newVal) {
      console.log('isSocio changed:', newVal);
    }
  },
  mounted() {
    console.log('Navbar mounted. Auth state:', {
      isAuthenticated: this.isAuthenticated,
      isAdmin: this.isAdmin,
      isSocio: this.isSocio
    });
  }
}
</script>

<style scoped>
.navbar {
  background-color: #333;
  padding: 1rem;
}
.navbar ul {
  list-style-type: none;
  display: flex;
  gap: 1rem;
}
.navbar a {
  color: white;
  text-decoration: none;
}
.debug-info {
  position: fixed;
  bottom: 10px;
  right: 10px;
  background-color: rgba(0,0,0,0.7);
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
}
</style>