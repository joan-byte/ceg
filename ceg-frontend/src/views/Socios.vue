<template>
  <div class="max-w-4xl mx-auto bg-white shadow-md rounded-lg p-6">
    <h1 class="text-2xl font-bold mb-4">Agregar Socio</h1>
    <form @submit.prevent="createSocio">
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
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-lastname">
          Apellido
        </label>
        <input
          v-model="lastname"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-lastname"
          name="lastname"
          type="text"
          placeholder="Apellido"
          autocomplete="family-name"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-email">
          Email
        </label>
        <input
          v-model="email"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-email"
          name="email"
          type="email"
          placeholder="Email"
          autocomplete="email"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-phone">
          Teléfono
        </label>
        <input
          v-model="phone"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-phone"
          name="phone"
          type="tel"
          placeholder="Teléfono"
          autocomplete="tel"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-password">
          Password
        </label>
        <input
          v-model="password"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-password"
          name="password"
          type="password"
          placeholder="Password"
          autocomplete="new-password"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="new-type">
          Tipo de Socio
        </label>
        <select
          v-model="type"
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="new-type"
          name="type"
        >
          <option value="">Seleccione el tipo de socio</option>
          <option value="Socio Deportivo">Socio Deportivo</option>
          <option value="Socio Paseante">Socio Paseante</option>
        </select>
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button"
          @click="createSocio"
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
    <h2 class="text-xl font-bold mb-4">Socios Existentes</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="socio in socios" :key="socio.id" class="bg-white shadow-md rounded-lg p-6">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'name-' + socio.id">
            Nombre
          </label>
          <input
            v-model="socio.name"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'name-' + socio.id"
            name="name"
            type="text"
            placeholder="Nombre"
            :readonly="!socio.isEditing"
            autocomplete="name"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'lastname-' + socio.id">
            Apellido
          </label>
          <input
            v-model="socio.lastname"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'lastname-' + socio.id"
            name="lastname"
            type="text"
            placeholder="Apellido"
            :readonly="!socio.isEditing"
            autocomplete="family-name"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'email-' + socio.id">
            Email
          </label>
          <input
            v-model="socio.email"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'email-' + socio.id"
            name="email"
            type="email"
            placeholder="Email"
            :readonly="!socio.isEditing"
            autocomplete="email"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'phone-' + socio.id">
            Teléfono
          </label>
          <input
            v-model="socio.phone"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'phone-' + socio.id"
            name="phone"
            type="tel"
            placeholder="Teléfono"
            :readonly="!socio.isEditing"
            autocomplete="tel"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'password-' + socio.id">
            Password
          </label>
          <input
            v-model="socio.password"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'password-' + socio.id"
            name="password"
            type="password"
            placeholder="Password"
            :readonly="!socio.isEditing"
            autocomplete="new-password"
          />
        </div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" :for="'type-' + socio.id">
            Tipo de Socio
          </label>
          <select
            v-model="socio.type"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            :id="'type-' + socio.id"
            name="type"
            :disabled="!socio.isEditing"
          >
            <option value="Socio Deportivo">Socio Deportivo</option>
            <option value="Socio Paseante">Socio Paseante</option>
          </select>
        </div>
        <div class="flex items-center justify-between mt-4">
          <template v-if="socio.isEditing">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              @click="saveSocio(socio.id, socio.name, socio.lastname, socio.email, socio.phone, socio.password, socio.type)"
            >
              Guardar
            </button>
            <button
              class="ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              @click="cancelEdit(socio.id)"
            >
              Cancelar
            </button>
          </template>
          <template v-else>
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              @click="editSocio(socio.id)"
            >
              Modificar
            </button>
            <button
              class="ml-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              @click="deleteSocio(socio.id)"
            >
              Eliminar
            </button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Socios',
  data() {
    return {
      name: '',
      lastname: '',
      email: '',
      phone: '',
      password: '',
      type: '',
      socios: []  // Lista de socios existentes
    }
  },
  methods: {
    createSocio() {
      const socioData = {
        name: this.name,
        lastname: this.lastname,
        email: this.email,
        phone: this.phone,
        password: this.password,
        type: this.type
      }
      axios.post('http://localhost:8000/socios/', socioData)
        .then(response => {
          alert('Socio creado con éxito')
          this.clearFields()
          this.fetchSocios()  // Actualizar la lista de socios
        })
        .catch(error => {
          console.error('Hubo un error al crear el socio:', error)
        })
    },
    clearFields() {
      this.name = ''
      this.lastname = ''
      this.email = ''
      this.phone = ''
      this.password = ''
      this.type = ''
    },
    fetchSocios() {
      axios.get('http://localhost:8000/socios/')
        .then(response => {
          this.socios = response.data.map(socio => ({ ...socio, isEditing: false }))
        })
        .catch(error => {
          console.error('Hubo un error al obtener los socios:', error)
        })
    },
    editSocio(socioId) {
      const socio = this.socios.find(socio => socio.id === socioId)
      socio.isEditing = true
    },
    cancelEdit(socioId) {
      const socio = this.socios.find(socio => socio.id === socioId)
      socio.isEditing = false
      this.fetchSocios()  // Revertir cambios si se cancela la edición
    },
    saveSocio(socioId, name, lastname, email, phone, password, type) {
      const socioData = {
        name: name,
        lastname: lastname,
        email: email,
        phone: phone,
        password: password,
        type: type
      }
      axios.put(`http://localhost:8000/socios/${socioId}`, socioData)
        .then(response => {
          alert('Socio modificado con éxito')
          this.fetchSocios()  // Actualizar la lista de socios
        })
        .catch(error => {
          console.error('Hubo un error al modificar el socio:', error)
        })
    },
    deleteSocio(socioId) {
      axios.delete(`http://localhost:8000/socios/${socioId}`)
        .then(response => {
          alert('Socio eliminado con éxito')
          this.fetchSocios()  // Actualizar la lista de socios
        })
        .catch(error => {
          console.error('Hubo un error al eliminar el socio:', error)
        })
    }
  },
  mounted() {
    this.fetchSocios()  // Obtener la lista de socios al cargar el componente
  }
}
</script>

<style scoped>
/* Puedes agregar estilos específicos para este componente aquí si es necesario */
</style>