<template>
  <div class="max-w-md mx-auto bg-white shadow-md rounded-lg p-6">
    <h1 class="text-2xl font-bold mb-4">Agregar Administrador</h1>
    <form @submit.prevent="createAdmin">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-name">
          Nombre
        </label>
        <input
          v-model="name"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-name"
          name="name"
          type="text"
          placeholder="Nombre"
          autocomplete="name"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-password">
          Password
        </label>
        <input
          v-model="password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="new-password"
          name="password"
          type="password"
          placeholder="Password"
          autocomplete="new-password"
        />
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button"
          @click="createAdmin"
        >
          Crear
        </button>
        <button
          class="ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button"
          @click="clearFields"
        >
          Cancelar
        </button>
      </div>
    </form>
  </div>

  <div class="mt-8">
    <h2 class="text-xl font-bold mb-4">Administradores Existentes</h2>
    <div v-for="admin in admins" :key="admin.id" class="max-w-md mx-auto bg-white shadow-md rounded-lg p-6 mb-4">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" :for="'name-' + admin.id">
          Nombre
        </label>
        <input
          v-model="admin.name"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          :id="'name-' + admin.id"
          name="name"
          type="text"
          placeholder="Nombre"
          :readonly="!admin.isEditing"
          autocomplete="name"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" :for="'password-' + admin.id">
          Password
        </label>
        <input
          v-model="admin.password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          :id="'password-' + admin.id"
          name="password"
          type="password"
          placeholder="Password"
          :readonly="!admin.isEditing"
          autocomplete="new-password"
        />
      </div>
      <div class="flex items-center justify-between mt-4">
        <template v-if="admin.isEditing">
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click="saveAdmin(admin.id, admin.name, admin.password)"
          >
            Guardar
          </button>
          <button
            class="ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click="cancelEdit(admin.id)"
          >
            Cancelar
          </button>
        </template>
        <template v-else>
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click="editAdmin(admin.id)"
          >
            Modificar
          </button>
          <button
            class="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            @click="deleteAdmin(admin.id)"
          >
            Eliminar
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Administradores',
  data() {
    return {
      name: '',
      password: '',
      admins: []  // Lista de administradores existentes
    }
  },
  methods: {
    createAdmin() {
      const adminData = {
        name: this.name,
        password: this.password
      }
      axios.post('http://localhost:8000/admins/', adminData)
        .then(response => {
          alert('Administrador creado con éxito')
          this.clearFields()
          this.fetchAdmins()  // Actualizar la lista de administradores
        })
        .catch(error => {
          console.error('Hubo un error al crear el administrador:', error)
        })
    },
    clearFields() {
      this.name = ''
      this.password = ''
    },
    fetchAdmins() {
      axios.get('http://localhost:8000/admins/')
        .then(response => {
          this.admins = response.data.map(admin => ({ ...admin, isEditing: false }))
        })
        .catch(error => {
          console.error('Hubo un error al obtener los administradores:', error)
        })
    },
    editAdmin(adminId) {
      const admin = this.admins.find(admin => admin.id === adminId)
      admin.isEditing = true
    },
    cancelEdit(adminId) {
      const admin = this.admins.find(admin => admin.id === adminId)
      admin.isEditing = false
      this.fetchAdmins()  // Revertir cambios si se cancela la edición
    },
    saveAdmin(adminId, name, password) {
      const adminData = {
        name: name,
        password: password
      }
      axios.put(`http://localhost:8000/admins/${adminId}`, adminData)
        .then(response => {
          alert('Administrador modificado con éxito')
          this.fetchAdmins()  // Actualizar la lista de administradores
        })
        .catch(error => {
          console.error('Hubo un error al modificar el administrador:', error)
        })
    },
    deleteAdmin(adminId) {
      axios.delete(`http://localhost:8000/admins/${adminId}`)
        .then(response => {
          alert('Administrador eliminado con éxito')
          this.fetchAdmins()  // Actualizar la lista de administradores
        })
        .catch(error => {
          console.error('Hubo un error al eliminar el administrador:', error)
        })
    }
  },
  mounted() {
    this.fetchAdmins()  // Obtener la lista de administradores al cargar el componente
  }
}
</script>

<style scoped>
/* Puedes agregar estilos específicos para este componente aquí si es necesario */
</style>