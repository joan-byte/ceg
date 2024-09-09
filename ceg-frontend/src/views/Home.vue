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
    <div v-else-if="Object.keys(reservasAgrupadasPorPista).length === 0" class="text-center py-4">
      <p>No hay reservas disponibles en las próximas 24 horas.</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
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
          <div v-if="isAdmin" class="mt-4 flex space-x-2">
            <button @click="editReserva(reserva)" class="px-4 py-1 bg-green-500 text-white rounded hover:bg-green-600">Modificar</button>
            <button @click="deleteReserva(reserva.id)" class="px-4 py-1 bg-red-500 text-white rounded hover:bg-red-600">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="userRoleLoaded" class="mt-4 text-sm">
      Estado de usuario: {{ userRole ? (userRole === 'admin' ? 'Administrador' : (userRole === 'socio' ? 'Socio' : 'No autenticado')) : 'No autenticado' }}
    </div>
    <div v-else>
      Cargando...
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const reservas = ref([]);
    const pistas = ref({});
    const error = ref(null);
    const isLoading = ref(true);
    const isAdmin = ref(false);
    const userRole = ref(null);
    const userRoleLoaded = ref(false);
    const router = useRouter();

    const checkUserStatus = async () => {
      const token = localStorage.getItem('token');
      const storedUserRole = localStorage.getItem('userRole');

      if (!token || !storedUserRole) {
        console.log('No hay token o rol de usuario');
        userRole.value = null;
        isAdmin.value = false;
      } else {
        try {
          if (storedUserRole === 'admin') {
            const response = await axios.get('http://localhost:8000/admin/check-role', {
              headers: { Authorization: `Bearer ${token}` }
            });
            isAdmin.value = response.data.is_admin;
            userRole.value = 'admin';
          } else if (storedUserRole === 'socio') {
            const response = await axios.get('http://localhost:8000/socios/me', {
              headers: { Authorization: `Bearer ${token}` }
            });
            if (response.data) {
              userRole.value = 'socio';
            }
          }
        } catch (err) {
          console.error('Error al verificar el estado de usuario:', err);
          userRole.value = null;
          isAdmin.value = false;
          localStorage.removeItem('token');
          localStorage.removeItem('userRole');
          router.push('/login');
        }
      }
      userRoleLoaded.value = true;
    };

    const fetchReservas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/reservas/');
        reservas.value = response.data;
      } catch (err) {
        console.error('Error al obtener las reservas:', err);
        error.value = 'Error al cargar las reservas. Por favor, intente más tarde.';
      } finally {
        isLoading.value = false;
      }
    };

    const fetchPistas = async () => {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
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
      if (!reservas.value.length) return {};
      
      const ahora = new Date();
      const en24Horas = new Date(ahora.getTime() + 24 * 60 * 60 * 1000);
      
      const reservasFiltradas = reservas.value.filter(reserva => {
        const fechaHoraInicio = new Date(reserva.dia + 'T' + reserva.hora_inicio);
        const fechaHoraFin = new Date(reserva.dia + 'T' + reserva.hora_fin);
        
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
      return timeString.slice(0, 5);
    };

    const editReserva = (reserva) => {
      if (isAdmin.value) {
        router.push({ name: 'EditarReserva', params: { id: reserva.id } });
      }
    };

    const deleteReserva = async (reservaId) => {
      if (isAdmin.value && confirm('¿Está seguro de que desea eliminar esta reserva?')) {
        try {
          const token = localStorage.getItem('token');
          await axios.delete(`http://localhost:8000/reservas/${reservaId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          await fetchReservas();
        } catch (err) {
          console.error('Error al eliminar la reserva:', err);
          error.value = 'Error al eliminar la reserva. Por favor, intente nuevamente.';
          if (err.response && err.response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('userRole');
            isAdmin.value = false;
          }
        }
      }
    };

    onMounted(async () => {
      await checkUserStatus();
      await Promise.all([fetchPistas(), fetchReservas()]);
    });

    watch(userRole, (newValue) => {
      console.log('userRole cambió a:', newValue);
    });

    return {
      reservasAgrupadasPorPista,
      getNombrePista,
      reservaEnCurso,
      formatDate,
      formatTime,
      error,
      isLoading,
      isAdmin,
      userRole,
      userRoleLoaded,
      editReserva,
      deleteReserva,
      checkUserStatus
    };
  },
  async mounted() {
    await this.cargarReservasActualizadas();
  },
  methods: {
    async cargarReservasActualizadas() {
      try {
        const response = await axios.get('http://localhost:8000/reservas/');
        // Actualizar el estado con las reservas más recientes
        this.reservas = response.data;
      } catch (error) {
        console.error("Error al cargar las reservas:", error);
      }
    }
  }
};
</script>