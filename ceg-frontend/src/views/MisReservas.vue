<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Mis Reservas</h1>
    <div v-if="isLoading">Cargando reservas...</div>
    <div v-else-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
    <div v-else-if="reservas.length === 0">No tienes reservas actualmente.</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="reserva in reservas" :key="reserva.id" class="bg-white shadow-md rounded-lg p-4">
        <h2 class="text-xl font-semibold mb-2">Reserva #{{ reserva.id }}</h2>
        <p><strong>Fecha:</strong> {{ formatDate(reserva.dia) }}</p>
        <p><strong>Hora:</strong> {{ reserva.hora_inicio }} - {{ reserva.hora_fin }}</p>
        <p><strong>Pista:</strong> {{ reserva.pista.name }}</p>
        <p><strong>Jugadores:</strong></p>
        <ul>
          <li v-for="jugador in reserva.jugadores" :key="jugador.id">{{ jugador.name }} {{ jugador.apellido }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      reservas: [],
      isLoading: true,
      errorMessage: '',
    };
  },
  methods: {
    async fetchMisReservas() {
  this.isLoading = true;
  this.errorMessage = '';
  try {
    console.log("Iniciando fetchMisReservas");
    const response = await axios.get('http://localhost:8000/reservas/mis-reservas', {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
    console.log("Respuesta recibida:", response.data);
    this.reservas = response.data;
    console.log("Reservas actualizadas:", this.reservas);
  } catch (error) {
    console.error('Error al obtener mis reservas:', error);
    if (error.response) {
      console.error('Respuesta del servidor:', error.response.data);
      console.error('Código de estado:', error.response.status);
      this.errorMessage = `Error ${error.response.status}: ${JSON.stringify(error.response.data)}`;
    } else if (error.request) {
      console.error('No se recibió respuesta:', error.request);
      this.errorMessage = 'No se pudo conectar con el servidor';
    } else {
      console.error('Error de configuración:', error.message);
      this.errorMessage = 'Error al procesar la solicitud';
    }
  } finally {
    this.isLoading = false;
  }
},
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    }
  },
  mounted() {
    this.fetchMisReservas();
  }
};
</script>