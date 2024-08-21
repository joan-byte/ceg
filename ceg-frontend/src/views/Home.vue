<template>
  <div class="container mx-auto px-4">
    <h1 class="text-3xl font-bold mb-6">Reservas próximas 24 horas</h1>
    <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div v-for="(pistaReservas, pistaId) in reservasAgrupadasPorPista" :key="pistaId" class="mb-6">
        <h2 class="text-xl font-semibold mb-3">{{ getNombrePista(pistaId) }}</h2>
        <div v-for="reserva in pistaReservas" :key="reserva.id" class="bg-white shadow-md rounded-lg p-4 mb-4">
          <div class="font-bold">{{ formatDate(reserva.dia) }}</div>
          <div>
            {{ formatTime(reserva.hora_inicio) }} - {{ formatTime(reserva.hora_fin) }}
            <span v-if="reservaEnCurso(reserva)" class="ml-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs">En curso</span>
          </div>
          <div v-for="jugador in reserva.jugadores" :key="jugador.id" class="text-sm">
            {{ jugador.name }} {{ jugador.apellido }} ({{ jugador.tipo_jugador }})
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const reservas = ref([]);
    const pistas = ref({});
    const error = ref(null);

    const fetchReservas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/reservas/');
        reservas.value = response.data;
        console.log('Datos de reservas recibidos:', response.data);
      } catch (err) {
        console.error('Error al obtener las reservas:', err);
        error.value = 'Error al cargar las reservas. Por favor, intente más tarde.';
      }
    };

    const fetchPistas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
        pistas.value = response.data.reduce((acc, pista) => {
          acc[pista.id] = pista.name;
          return acc;
        }, {});
        console.log('Datos de pistas recibidos:', pistas.value);
      } catch (err) {
        console.error('Error al obtener las pistas:', err);
        error.value = 'Error al cargar las pistas. Por favor, intente más tarde.';
      }
    };

    const reservasAgrupadasPorPista = computed(() => {
      const ahora = new Date();
      const en24Horas = new Date(ahora.getTime() + 24 * 60 * 60 * 1000);
      
      const reservasFiltradas = reservas.value.filter(reserva => {
        const fechaHoraInicio = new Date(reserva.dia + 'T' + reserva.hora_inicio);
        const fechaHoraFin = new Date(reserva.dia + 'T' + reserva.hora_fin);
        
        // Incluir reservas en curso o que comienzan en las próximas 24 horas
        return (fechaHoraInicio <= ahora && fechaHoraFin > ahora) || 
               (fechaHoraInicio > ahora && fechaHoraInicio < en24Horas);
      });

      const agrupadas = {};
      reservasFiltradas.forEach(reserva => {
        const pistaId = reserva.pista_id;
        if (!agrupadas[pistaId]) {
          agrupadas[pistaId] = [];
        }
        agrupadas[pistaId].push(reserva);
      });

      // Ordenar las reservas por fecha y hora dentro de cada pista
      for (let pista in agrupadas) {
        agrupadas[pista].sort((a, b) => {
          const dateA = new Date(a.dia + 'T' + a.hora_inicio);
          const dateB = new Date(b.dia + 'T' + b.hora_inicio);
          return dateA - dateB;
        });
      }

      return agrupadas;
    });

    const getNombrePista = (pistaId) => {
      return pistas.value[pistaId] || `Pista ${pistaId}`;
    };

    const reservaEnCurso = (reserva) => {
      const ahora = new Date();
      const fechaHoraInicio = new Date(reserva.dia + 'T' + reserva.hora_inicio);
      const fechaHoraFin = new Date(reserva.dia + 'T' + reserva.hora_fin);
      return fechaHoraInicio <= ahora && fechaHoraFin > ahora;
    };

    const formatDate = (dateString) => {
      const options = { weekday: 'long', day: 'numeric', month: 'long' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    };

    const formatTime = (timeString) => {
      return timeString.slice(0, 5); // Asumiendo que el formato es "HH:MM:SS"
    };

    onMounted(async () => {
      await fetchPistas();
      await fetchReservas();
    });

    return {
      reservasAgrupadasPorPista,
      getNombrePista,
      reservaEnCurso,
      formatDate,
      formatTime,
      error,
    };
  }
};
</script>