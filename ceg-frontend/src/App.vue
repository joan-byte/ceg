<template>
  <div>
    <Navbar :isAdmin="isAdmin" :isSocio="isSocio" />
    <div class="p-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  data() {
    return {
      isAdmin: true, // Cambia esto según la lógica de autenticación
      isSocio: true  // Cambia esto según la lógica de autenticación
    }
  }
}
</script>

<style>
/* Puedes agregar estilos globales aquí si es necesario */
</style>