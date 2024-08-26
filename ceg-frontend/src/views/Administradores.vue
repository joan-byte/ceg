<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Gestión de Administradores</h1>
    <form @submit.prevent="submitForm" class="mb-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Username</label>
          <input v-model="form.username" type="text" class="mt-1 block w-full" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input v-model="form.email" type="email" class="mt-1 block w-full" required />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Password</label>
          <input v-model="form.password" type="password" class="mt-1 block w-full" required />
        </div>
      </div>
      <div class="mt-6">
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Guardar</button>
      </div>
    </form>

    <h2 class="text-2xl font-bold mb-4">Lista de Administradores</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div v-for="admin in admins" :key="admin.id" class="bg-white p-4 rounded shadow">
        <h3 class="text-lg font-bold">{{ admin.username }}</h3>
        <p>{{ admin.email }}</p>
        <button @click="editAdmin(admin)" class="mt-2 px-4 py-1 bg-green-500 text-white rounded">Editar</button>
        <button @click="deleteAdmin(admin.id)" class="mt-2 px-4 py-1 bg-red-500 text-white rounded">Eliminar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        email: '', // Nuevo campo de email
        password: '',
      },
      admins: [] // Lista de administradores
    }
  },
  methods: {
    submitForm() {
      // Lógica para guardar o actualizar el administrador
      if (this.form.id) {
        // Actualizar administrador existente
        this.updateAdmin()
      } else {
        // Crear nuevo administrador
        this.createAdmin()
      }
    },
    createAdmin() {
      // Llamada al backend para crear un nuevo administrador
      // Enviar this.form con username, email y password
    },
    updateAdmin() {
      // Llamada al backend para actualizar un administrador existente
      // Enviar this.form con username, email y password
    },
    editAdmin(admin) {
      this.form = { ...admin } // Cargar datos del administrador en el formulario
    },
    deleteAdmin(id) {
      // Llamada al backend para eliminar un administrador
    }
  },
  mounted() {
    // Lógica para cargar la lista de administradores desde el backend
  }
}
</script>

<style scoped>
/* Mantén aquí los estilos existentes sin cambios */
</style>