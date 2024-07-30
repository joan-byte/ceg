<template>
  <nav class="bg-blue-500 p-4">
    <ul class="flex space-x-4">
      <li><router-link to="/" class="text-white">Reservas</router-link></li>
      <li><router-link to="/register" class="text-white">Register</router-link></li>
      <li><router-link to="/login" class="text-white">Login</router-link></li>
      <li><a @click="logout" class="text-white cursor-pointer">Logout</a></li>
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
</template>

<script>
export default {
  props: {
    isAdmin: {
      type: Boolean,
      default: false
    },
    isSocio: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    logout() {
      // Aquí debería ir la lógica de cierre de sesión
      this.$router.push('/login')
    }
  }
}
</script>