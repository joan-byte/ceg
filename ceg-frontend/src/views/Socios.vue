<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Gestión de Socios</h1>

    <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline">{{ errorMessage }}</span>
    </div>

    <!-- Formulario para crear/editar socio -->
    <form @submit.prevent="submitForm" class="mb-8 login-container max-w-2xl">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Nombre</label>
          <input type="text" id="name" v-model="form.name" required class="mt-1 block w-full" autocomplete="off">
        </div>
        <div>
          <label for="lastname" class="block text-sm font-medium text-gray-700">Apellido</label>
          <input type="text" id="lastname" v-model="form.lastname" required class="mt-1 block w-full" autocomplete="off">
        </div>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" id="email" v-model="form.email" required class="mt-1 block w-full" autocomplete="email">
        </div>
        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700">Teléfono</label>
          <input type="tel" id="phone" v-model="form.phone" required class="mt-1 block w-full" autocomplete="tel">
        </div>
      </div>
      <div class="mt-4">
        <label for="type" class="block text-sm font-medium text-gray-700">Tipo de Socio</label>
        <select id="type" v-model="form.type" required class="mt-1 block w-full" autocomplete="off">
          <option value="Socio Deportivo">Socio Deportivo</option>
          <option value="Socio Paseante">Socio Paseante</option>
        </select>
      </div>
      <div class="mt-4" v-if="!currentSocio">
        <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
        <input type="password" id="password" v-model="form.password" required class="mt-1 block w-full" autocomplete="new-password">
      </div>
      <div class="mt-4" v-else>
        <label for="new_password" class="block text-sm font-medium text-gray-700">Nueva Contraseña (dejar en blanco para no cambiar)</label>
        <input type="password" id="new_password" v-model="form.new_password" class="mt-1 block w-full" autocomplete="new-password">
      </div>
      <div class="mt-6 flex flex-col items-start space-y-2">
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
          {{ currentSocio ? 'Modificar' : 'Crear' }}
        </button>
        <button v-if="currentSocio" @click="cancelEdit" type="button" class="px-4 py-2 bg-gray-500 text-white rounded">
          Cancelar
        </button>
      </div>
    </form>

    <!-- Lista de socios -->
    <h2 class="text-2xl font-bold mb-4">Lista de Socios</h2>
    <div v-if="isLoading" class="text-center">
      <p>Cargando socios...</p>
    </div>
    <div v-else-if="socios.length === 0" class="text-center">
      <p>No hay socios registrados.</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 justify-center">
      <div v-for="socio in socios" :key="socio.id" class="bg-white p-4 rounded shadow w-full max-w-xs h-64 flex flex-col justify-between">
        <div>
          <h3 class="text-lg font-bold">{{ socio.name }} {{ socio.lastname }}</h3>
          <p>Email: {{ socio.email }}</p>
          <p>Teléfono: {{ socio.phone }}</p>
          <p>Tipo: {{ socio.type }}</p>
        </div>
        <div class="flex space-x-2 mt-4">
          <button @click="editSocio(socio)" class="px-4 py-1 bg-green-500 text-white rounded">Modificar</button>
          <button @click="deleteSocio(socio.id)" class="px-4 py-1 bg-red-500 text-white rounded">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import '../styles/login.css';

export default {
  data() {
    return {
      socios: [],
      form: {
        name: '',
        lastname: '',
        email: '',
        phone: '',
        password: '',
        new_password: '',
        type: 'Socio Deportivo',
      },
      currentSocio: null,
      isLoading: false,
      errorMessage: ''
    };
  },
  methods: {
    getToken() {
      const tokenData = localStorage.getItem('token');
      if (!tokenData) {
        throw new Error('No se encontró el token de autenticación');
      }
      return tokenData;
    },
    async fetchSocios() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const token = this.getToken();
        const response = await axios.get('http://localhost:8000/socios/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.socios = response.data;
        console.log('Socios actualizados:', this.socios);
      } catch (error) {
        console.error('Error al obtener socios:', error);
        this.errorMessage = 'Error al obtener la lista de socios.';
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'No autorizado. Por favor, inicie sesión nuevamente.';
          // Redirigir a la página de inicio de sesión o manejar el error
        }
      } finally {
        this.isLoading = false;
      }
    },
    async submitForm() {
      if (this.currentSocio) {
        this.updateSocio();
      } else {
        this.createSocio();
      }
    },
    async createSocio() {
      try {
        const token = this.getToken();
        const response = await axios.post('http://localhost:8000/socios/', this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });
        this.socios.push(response.data);
        this.resetForm();
        this.errorMessage = '';
      } catch (error) {
        console.error('Error al crear socio:', error.response?.data || error.message);
        this.errorMessage = 'Error al crear socio. Por favor, verifique los datos e intente nuevamente.';
      }
    },
    async updateSocio() {
      try {
        console.log('Datos a enviar:', this.form);
        const response = await axios.put(`http://localhost:8000/socios/${this.currentSocio.id}`, this.form, {
          headers: {
            Authorization: `Bearer ${this.getToken()}`,
            'Content-Type': 'application/json'
          },
        });
        console.log('Respuesta del servidor:', response.data);
        // Actualizar el socio en la lista local
        const index = this.socios.findIndex(s => s.id === this.currentSocio.id);
        if (index !== -1) {
          this.socios[index] = response.data;
        }
        this.resetForm();
        this.successMessage = 'Socio actualizado correctamente';
        await this.fetchSocios();
      } catch (error) {
        console.error('Error al actualizar socio:', error);
        if (error.response) {
          // El servidor respondió con un estado fuera del rango de 2xx
          console.error('Respuesta del servidor:', error.response.data);
          this.errorMessage = `Error al actualizar socio: ${error.response.data.detail}`;
        } else if (error.request) {
          // La solicitud fue hecha pero no se recibió respuesta
          this.errorMessage = 'No se recibió respuesta del servidor. Por favor, intente nuevamente.';
        } else {
          // Algo sucedió al configurar la solicitud que provocó un error
          this.errorMessage = 'Error al enviar la solicitud. Por favor, intente nuevamente.';
        }
      }
    },
    editSocio(socio) {
      this.currentSocio = { ...socio };
      this.form = { 
        name: socio.name,
        lastname: socio.lastname,
        email: socio.email,
        phone: socio.phone,
        type: socio.type,
        new_password: ''
      };
    },
    cancelEdit() {
      this.resetForm();
    },
    async deleteSocio(socioId) {
      if (confirm('¿Está seguro de que desea eliminar este socio?')) {
        try {
          const token = this.getToken();
          await axios.delete(`http://localhost:8000/socios/${socioId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.socios = this.socios.filter(s => s.id !== socioId);
          this.errorMessage = '';
        } catch (error) {
          console.error('Error al eliminar socio:', error.response?.data || error.message);
          this.errorMessage = 'Error al eliminar socio. Por favor, intente nuevamente.';
        }
      }
    },
    resetForm() {
      this.form = {
        name: '',
        lastname: '',
        email: '',
        phone: '',
        password: '',
        new_password: '',
        type: 'Socio Deportivo',
      };
      this.currentSocio = null;
      this.errorMessage = '';
      this.successMessage = '';
    },
  },
  async mounted() {
    await this.fetchSocios();
  },
};
</script>

<style scoped>
/* Importamos el CSS desde login.css */
</style>