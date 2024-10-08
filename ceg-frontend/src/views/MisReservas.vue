<template>
  <div class="container mx-auto mt-8">
    <h1 class="text-3xl font-bold mb-6">Mis Reservas</h1>
    <div v-if="isLoading">Cargando reservas...</div>
    <div v-else-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
    <div v-else-if="Object.keys(reservasAgrupadasPorPista).length === 0">No tienes reservas actualmente.</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="(pistaReservas, pistaId) in reservasAgrupadasPorPista" :key="pistaId" class="mb-6">
        <h2 class="text-xl font-semibold mb-3">{{ getNombrePista(pistaId) }}</h2>
        <div class="grid grid-cols-1 gap-4">
          <div v-for="reserva in pistaReservas" :key="reserva.id" class="bg-white shadow-md rounded-lg p-4 flex flex-col justify-between h-64 w-full">
            <div class="flex flex-col h-full">
              <div class="font-bold">{{ formatDate(reserva.dia) }}</div>
              <div>{{ reserva.hora_inicio }} - {{ reserva.hora_fin }}</div>
              <div class="flex-grow overflow-y-auto">
                <p><strong>Jugadores:</strong></p>
                <ul>
                  <li v-for="jugador in reserva.jugadores" :key="jugador.id">{{ jugador.name }} {{ jugador.apellido }}</li>
                </ul>
              </div>
            </div>
            <div class="mt-2 flex space-x-2">
              <button @click="editReserva(reserva.id)" class="px-4 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm">
                Modificar
              </button>
              <button @click="deleteReserva(reserva.id)" class="px-4 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm">
                Eliminar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    return { router };
  },
  data() {
    return {
      reservas: [],
      pistas: {},
      isLoading: true,
      errorMessage: '',
    };
  },
  computed: {
    reservasAgrupadasPorPista() {
      const agrupadas = {};
      this.reservas.forEach(reserva => {
        const pistaId = reserva.pista.id;
        if (!agrupadas[pistaId]) {
          agrupadas[pistaId] = [];
        }
        agrupadas[pistaId].push(reserva);
      });

      // Ordenar las reservas por fecha y hora
      for (let pista in agrupadas) {
        agrupadas[pista].sort((a, b) => {
          const dateA = new Date(a.dia + 'T' + a.hora_inicio);
          const dateB = new Date(b.dia + 'T' + b.hora_inicio);
          return dateA - dateB;
        });
      }

      return agrupadas;
    },
  },
  methods: {
    async fetchMisReservas() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const response = await axios.get('http://localhost:8000/reservas/mis-reservas', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.reservas = response.data;
        console.log("Reservas cargadas:", this.reservas);
      } catch (error) {
        console.error('Error al obtener mis reservas:', error);
        if (error.response) {
          this.errorMessage = `Error ${error.response.status}: ${JSON.stringify(error.response.data)}`;
        } else if (error.request) {
          this.errorMessage = 'No se pudo conectar con el servidor';
        } else {
          this.errorMessage = 'Error al procesar la solicitud';
        }
      } finally {
        this.isLoading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    editReserva(reservaId) {
      this.router.push({
        name: 'EditarMiReserva',
        params: { id: reservaId.toString() }
      }).catch(err => {
        if (err.name !== 'NavigationDuplicated') {
          console.error(err);
        }
      });
    },
    async deleteReserva(reservaId) {
      if (confirm('¿Está seguro de que desea eliminar esta reserva?')) {
        try {
          await axios.delete(`http://localhost:8000/reservas/${reservaId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          await this.fetchMisReservas(); // Recargar las reservas después de eliminar
        } catch (error) {
          console.error('Error al eliminar la reserva:', error);
          alert('Error al eliminar la reserva. Por favor, intente nuevamente.');
        }
      }
    },
    getNombrePista(pistaId) {
      return this.pistas[pistaId] || `Pista ${pistaId}`;
    },
    async fetchPistas() {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
        this.pistas = response.data.reduce((acc, pista) => {
          acc[pista.id] = pista.name;
          return acc;
        }, {});
      } catch (error) {
        console.error('Error al obtener las pistas:', error);
        this.errorMessage = 'Error al cargar las pistas. Por favor, intente más tarde.';
      }
    },
  },
  async mounted() {
    await this.fetchPistas();
    await this.fetchMisReservas();
  }
};
</script>