<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Mis Reservas</h1>

    <div v-if="isLoading" class="text-center">
      <p>Cargando reservas...</p>
    </div>
    <div v-else-if="errorMessage" class="text-center text-red-500">
      <p>{{ errorMessage }}</p>
    </div>
    <div v-else-if="misReservas.length === 0" class="text-center">
      <p>No tienes reservas activas.</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="reserva in misReservas" :key="reserva.id" class="bg-white p-4 rounded shadow">
        <h2 class="text-xl font-semibold mb-2">Pista: {{ reserva.pista.name }}</h2>
        <p>Fecha: {{ formatDate(reserva.dia) }}</p>
        <p>Hora: {{ formatTime(reserva.hora_inicio) }} - {{ formatTime(reserva.hora_fin) }}</p>
        <h3 class="font-semibold mt-2">Jugadores:</h3>
        <ul>
          <li v-for="jugador in reserva.jugadores" :key="jugador.id">
            {{ jugador.name }} {{ jugador.apellido }} ({{ jugador.tipo_jugador }})
          </li>
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
      misReservas: [],
      isLoading: true,
      errorMessage: ''
    };
  },
  methods: {
    async fetchMisReservas() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/reservas/mis-reservas', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.misReservas = response.data;
      } catch (error) {
        console.error('Error al obtener mis reservas:', error);
        if (error.response) {
          console.log('Respuesta del servidor:', error.response.data);
          this.errorMessage = 'No se pudieron cargar las reservas. Por favor, intenta de nuevo más tarde.';
        }
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
    formatTime(timeString) {
      return timeString.slice(0, 5); // Asumiendo que el formato es "HH:MM:SS"
    }
  },
  mounted() {
    this.fetchMisReservas();
  }
};
</script>