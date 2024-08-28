<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Gestión de Administradores</h1>
    <form @submit.prevent="submitForm" class="mb-8 login-container max-w-2xl">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="admin-name" class="block text-sm font-medium text-gray-700">Nombre de Usuario</label>
          <input id="admin-name" name="name" v-model="form.name" :readonly="!!currentAdmin" type="text" class="mt-1 block w-full" required autocomplete="username" />
        </div>
        <div>
          <label for="admin-email" class="block text-sm font-medium text-gray-700">Correo Electrónico</label>
          <input id="admin-email" name="email" v-model="form.email" type="email" class="mt-1 block w-full" required autocomplete="email" />
        </div>
      </div>
      
      <div v-if="!currentAdmin" class="mt-4">
        <label for="admin-password" class="block text-sm font-medium text-gray-700">Contraseña</label>
        <input 
          id="admin-password" 
          name="password" 
          v-model="form.password" 
          type="password" 
          class="mt-1 block w-full" 
          required
          autocomplete="new-password" 
        />
      </div>
      
      <div v-if="currentAdmin" class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="admin-hashed-password" class="block text-sm font-medium text-gray-700">Contraseña Actual (Hasheada)</label>
          <input 
            id="admin-hashed-password" 
            name="hashed_password" 
            v-model="form.hashed_password" 
            type="password" 
            class="mt-1 block w-full" 
            readonly
          />
        </div>
        <div>
          <label for="admin-new-password" class="block text-sm font-medium text-gray-700">Nueva Contraseña</label>
          <input 
            id="admin-new-password" 
            name="new_password" 
            v-model="form.new_password" 
            type="password" 
            class="mt-1 block w-full" 
            autocomplete="new-password" 
            placeholder="Dejar en blanco para no cambiar"
          />
        </div>
      </div>
      
      <div class="mt-6 flex flex-col items-start space-y-2">
        <button v-if="currentAdmin" @click="cancelEdit" class="px-4 py-2 bg-gray-500 text-white rounded">Cancelar</button>
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">
          {{ currentAdmin ? 'Modificar' : 'Crear' }}
        </button>
      </div>
    </form>

    <!-- Lista de administradores -->
    <h2 class="text-2xl font-bold mb-4">Lista de Administradores</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 justify-center">
      <div v-for="admin in admins" :key="admin.id" class="bg-white p-4 rounded shadow w-full max-w-xs h-48 flex flex-col justify-between">
        <div>
          <h3 class="text-lg font-bold">{{ admin.name }}</h3>
          <p>Email: {{ admin.email }}</p>
          <div>
            <label :for="'admin-password-' + admin.id" class="block text-sm font-medium text-gray-700">Contraseña (Hasheada)</label>
            <input 
              :id="'admin-password-' + admin.id" 
              type="password" 
              :value="admin.hashed_password" 
              readonly 
              class="mt-1 block w-full border-none bg-transparent" 
            />
          </div>
        </div>
        <div class="flex space-x-2 mt-4">
          <button @click="editAdmin(admin)" class="px-4 py-1 bg-green-500 text-white rounded">Modificar</button>
          <button @click="deleteAdmin(admin.id)" class="px-4 py-1 bg-red-500 text-white rounded">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import '../styles/login.css'

export default {
  data() {
    return {
      admins: [],
      form: {
        name: '',
        email: '',
        hashed_password: '',
        new_password: '',
      },
      currentAdmin: null,
      isLoading: false,
      errorMessage: ''
    };
  },
  methods: {
    async fetchAdmins() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/admin/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.admins = response.data;
        console.log('Administradores obtenidos:', this.admins);
      } catch (error) {
        console.error('Error al obtener administradores:', error);
      }
    },
    async submitForm() {
      if (this.currentAdmin) {
        await this.updateAdmin();
      } else {
        await this.createAdmin();
      }
    },
    async createAdmin() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:8000/admin/', {
          name: this.form.name,
          email: this.form.email,
          password: this.form.new_password,
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });
        if (response.data) {
          this.admins.push(response.data);
          this.resetForm();
        }
      } catch (error) {
        console.error('Error al crear administrador:', error.response?.data || error.message);
      }
    },
    async updateAdmin() {
      try {
        const token = localStorage.getItem('token');

        const updateData = {
          name: this.currentAdmin.name,
          email: this.form.email,
        };

        if (this.form.new_password.trim() !== '') {
          updateData.password = this.form.new_password;
        }

        console.log('Datos a enviar para actualización:', updateData);

        const response = await axios.put(`http://localhost:8000/admin/${this.currentAdmin.id}`, updateData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });

        console.log('Respuesta del servidor tras actualización:', response.data);

        const index = this.admins.findIndex(a => a.id === this.currentAdmin.id);
        if (index !== -1) {
          this.admins[index] = { ...this.admins[index], ...response.data };
        }

        this.resetForm();
        await this.fetchAdmins();
      } catch (error) {
        console.error('Error al actualizar administrador:', error.response?.data || error.message);
      }
    },
    editAdmin(admin) {
      this.currentAdmin = { ...admin };
      this.form.name = admin.name;
      this.form.email = admin.email;
      this.form.hashed_password = admin.hashed_password;
      this.form.new_password = ''; // Limpiamos el campo de nueva contraseña
    },
    cancelEdit() {
      this.resetForm();
    },
    async deleteAdmin(adminId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:8000/admin/${adminId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.admins = this.admins.filter(a => a.id !== adminId);
      } catch (error) {
        console.error('Error al eliminar administrador:', error.response?.data || error.message);
      }
    },
    resetForm() {
      this.form = {
        name: '',
        email: '',
        hashed_password: '',
        new_password: '',
      };
      this.currentAdmin = null;
    },
  },
  async mounted() {
    await this.fetchAdmins();
  },
};
</script>

<style scoped>
/* Importamos el CSS desde login.css */
</style>