<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold">Cerrando sesión...</h1>
  </div>
</template>

<script>
export default {
  name: 'Logout',
  created() {
    // Limpiar el almacenamiento local
    localStorage.removeItem('token');
    localStorage.removeItem('userRole');
    
    // Redirigir a la página de inicio y recargar
    window.location.href = '/';
  }
}
</script>