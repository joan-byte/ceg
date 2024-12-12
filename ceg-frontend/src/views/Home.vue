<template>
  <div class="container mx-auto px-4 mt-8">
    <h1 class="text-3xl font-bold mb-6">Reservas próximas 24 horas</h1>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
      <strong class="font-bold">Error:</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>
    <div v-if="isLoading" class="text-center py-4">
      <p>Cargando reservas...</p>
    </div>
    <div v-if="Object.keys(reservasAgrupadasPorPista).length === 0" class="text-center py-4">
      <p>No hay reservas disponibles en las próximas 24 horas.</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="(pistaReservas, pistaId) in reservasAgrupadasPorPista" :key="pistaId" class="flex flex-col">
        <h2 class="text-xl font-semibold mb-3">{{ getNombrePista(pistaId) }}</h2>
        <div class="flex-grow flex flex-col gap-4">
          <div v-for="reserva in pistaReservas" :key="reserva.id" 
               class="bg-white shadow-md rounded-lg p-4 mb-4 flex flex-col justify-between h-64">
            <div>
              <p class="mb-1">{{ formatDate(reserva.dia) }}</p>
              <p class="mb-1">{{ formatTime(reserva.hora_inicio) }} - {{ formatTime(reserva.hora_fin) }}</p>
              <p v-if="isReservaEnCurso(reserva)" class="text-green-600 font-bold mb-1">En curso</p>
              <ul class="list-disc list-inside overflow-y-auto max-h-24">
                <li v-for="jugador in reserva.jugadores" :key="jugador.id">
                  {{ jugador.name }} {{ jugador.apellido }} ({{ jugador.tipo_jugador }})
                </li>
              </ul>
            </div>
            <div v-if="mostrarBotonesAdmin" class="mt-2 flex justify-end space-x-2">
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
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const reservas = ref([]);
    const pistas = ref({});
    const error = ref(null);
    const isLoading = ref(true);
    const mostrarBotonesAdmin = ref(false);
    const router = useRouter();

    const verificarAdmin = async () => {
      const token = localStorage.getItem('token') || sessionStorage.getItem('token');
      const userRole = localStorage.getItem('userRole') || sessionStorage.getItem('userRole');

      if (!token || userRole !== 'admin') {
        mostrarBotonesAdmin.value = false;
        return;
      }

      try {
        const response = await axios.get('http://192.168.10.21:8000/admin/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        mostrarBotonesAdmin.value = !!response.data;
      } catch (error) {
        console.error('Error verificando admin:', error);
        mostrarBotonesAdmin.value = false;
      }
    };

    const fetchReservas = async () => {
      try {
        const response = await axios.get('http://192.168.10.21:8000/reservas/');
        
        reservas.value = response.data.map(r => {
          // Crear objeto Date para la fecha
          const fecha = new Date(r.dia);
          
          // Extraer horas y minutos de inicio
          const [horaInicio, minInicio] = r.hora_inicio.split(':').map(Number);
          const inicioDate = new Date(fecha);
          inicioDate.setHours(horaInicio, minInicio, 0);
          
          // Extraer horas y minutos de fin
          const [horaFin, minFin] = r.hora_fin.split(':').map(Number);
          const finDate = new Date(fecha);
          finDate.setHours(horaFin, minFin, 0);
          
          // Si la hora de fin es menor que la hora de inicio, ajustar al día siguiente
          if (finDate <= inicioDate) {
            finDate.setDate(finDate.getDate() + 1);
          }
          
          return {
            ...r,
            dia: fecha,
            hora_inicio: r.hora_inicio.slice(0, 5),
            hora_fin: r.hora_fin.slice(0, 5),
            _fechaInicio: inicioDate,
            _fechaFin: finDate
          };
        });
      } catch (err) {
        console.error('Error al obtener las reservas:', err);
        error.value = 'Error al cargar las reservas. Por favor, intente más tarde.';
      } finally {
        isLoading.value = false;
      }
    };

    const fetchPistas = async () => {
      try {
        const response = await axios.get('http://192.168.10.21:8000/pistas/');
        pistas.value = response.data.reduce((acc, pista) => {
          acc[pista.id] = pista.name;
          return acc;
        }, {});
      } catch (err) {
        console.error('Error al obtener las pistas:', err);
        error.value = 'Error al cargar las pistas. Por favor, intente más tarde.';
      }
    };

    const reservasAgrupadasPorPista = computed(() => {
      const agrupadas = {};
      reservas.value.forEach(reserva => {
        if (!agrupadas[reserva.pista_id]) {
          agrupadas[reserva.pista_id] = [];
        }
        agrupadas[reserva.pista_id].push(reserva);
      });
      return agrupadas;
    });

    const getNombrePista = (pistaId) => {
      return pistas.value[pistaId] || `Pista ${pistaId}`;
    };

    const isReservaEnCurso = (reserva) => {
      const ahora = new Date();
      return ahora >= reserva._fechaInicio && ahora <= reserva._fechaFin;
    };

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const formatTime = (timeString) => {
      return timeString.slice(0, 5);
    };

    const editReserva = (reservaId) => {
      if (mostrarBotonesAdmin.value) {
        router.push({ name: 'EditarReserva', params: { id: reservaId.toString() } });
      }
    };

    const deleteReserva = async (reservaId) => {
      if (!mostrarBotonesAdmin.value) return;

      if (confirm('¿Está seguro de que desea eliminar esta reserva?')) {
        try {
          const token = localStorage.getItem('token') || sessionStorage.getItem('token');
          await axios.delete(`http://192.168.10.21:8000/reservas/${reservaId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          await fetchReservas();
        } catch (err) {
          console.error('Error al eliminar la reserva:', err);
          error.value = 'Error al eliminar la reserva. Por favor, intente nuevamente.';
        }
      }
    };

    onMounted(async () => {
      await verificarAdmin();
      await Promise.all([fetchPistas(), fetchReservas()]);
    });

    return {
      reservas,
      error,
      isLoading,
      mostrarBotonesAdmin,
      reservasAgrupadasPorPista,
      getNombrePista,
      isReservaEnCurso,
      formatDate,
      formatTime,
      editReserva,
      deleteReserva
    };
  }
};
</script>