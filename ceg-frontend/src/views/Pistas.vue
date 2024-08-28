<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Gestión de Pistas</h1>
    <form @submit.prevent="submitForm" class="mb-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700">Nombre de la Pista</label>
          <input id="name" name="name" v-model="form.name" type="text" class="mt-1 block w-full" required autocomplete="off" />
        </div>
        <div>
          <label for="tipo_pista" class="block text-sm font-medium text-gray-700">Tipo de Pista</label>
          <select id="tipo_pista" name="tipo_pista" v-model="form.tipo_pista" class="mt-1 block w-full" required autocomplete="off">
            <option disabled value="">Elige un tipo de pista</option>
            <option value="Tenis">Tenis</option>
            <option value="Padel">Padel</option>
            <option value="Pickleball">Pickleball</option>
          </select>
        </div>
        <div>
          <label for="tiempo_juego" class="block text-sm font-medium text-gray-700">Tiempo de Juego (minutos)</label>
          <input id="tiempo_juego" name="tiempo_juego" v-model="form.tiempo_juego" type="number" min="1" class="mt-1 block w-full" required autocomplete="off" />
        </div>
        <div class="flex items-center">
          <input id="individuales" name="individuales" v-model="form.individuales" type="checkbox" class="mt-1" />
          <label for="individuales" class="block text-sm font-medium text-gray-700 ml-2">Permite Individuales</label>
        </div>
      </div>
      <div class="mt-6">
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Guardar</button>
      </div>
    </form>

    <h2 class="text-2xl font-bold mb-4">Lista de Pistas</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 justify-center">
      <div v-for="pista in pistas" :key="pista.id" class="bg-white p-4 rounded shadow w-full">
        <h3 class="text-lg font-bold">{{ pista.name }}</h3>
        <p>Tipo: {{ pista.tipo_pista }}</p>
        <p>Tiempo de Juego: {{ pista.tiempo_juego }} minutos</p>
        <p>Permite Individuales: {{ pista.individuales ? 'Sí' : 'No' }}</p>
        <div class="flex space-x-2 mt-4"> <!-- Contenedor de botones con separación entre ellos -->
          <button @click="editPista(pista)" class="px-4 py-1 bg-green-500 text-white rounded">Modificar</button>
          <button @click="deletePista(pista.id)" class="px-4 py-1 bg-red-500 text-white rounded">Eliminar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      pistas: [],
      form: {
        name: '',
        tipo_pista: '',
        tiempo_juego: '',
        individuales: false,
      },
      currentPista: null,
    };
  },
  methods: {
    async fetchPistas() {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
        this.pistas = response.data;
      } catch (error) {
        console.error('Error fetching pistas:', error);
      }
    },
    async submitForm() {
      if (this.currentPista) {
        await this.updatePista();
      } else {
        await this.createPista();
      }
    },
    async createPista() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:8000/pistas/', this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.pistas.push(response.data);
        this.resetForm();
      } catch (error) {
        console.error('Error creating pista:', error);
      }
    },
    async updatePista() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.put(`http://localhost:8000/pistas/${this.currentPista.id}`, this.form, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const index = this.pistas.findIndex(p => p.id === this.currentPista.id);
        if (index !== -1) {
          this.$set(this.pistas, index, response.data);
        }
        this.resetForm();
      } catch (error) {
        console.error('Error updating pista:', error);
      }
    },
    editPista(pista) {
      this.currentPista = pista;
      this.form = { ...pista };
    },
    async deletePista(pistaId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://localhost:8000/pistas/${pistaId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        this.pistas = this.pistas.filter(p => p.id !== pistaId);
      } catch (error) {
        console.error('Error deleting pista:', error);
      }
    },
    resetForm() {
      this.form = {
        name: '',
        tipo_pista: '',
        tiempo_juego: '',
        individuales: false,
      };
      this.currentPista = null;
    },
  },
  async mounted() {
    await this.fetchPistas();
  },
};
</script>

<style scoped>
.container {
  max-width: 800px;
}
/* Mantén los estilos existentes o añade más aquí según sea necesario */
</style>