<template>
  <div class="container mx-auto mt-8 px-4">
    <h1 class="text-3xl font-bold mb-6">Mis Reservas</h1>
    <div v-if="isLoading" class="text-center py-4">
      <p>Cargando reservas...</p>
    </div>
    <div v-else-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
      {{ errorMessage }}
    </div>
    <div v-else-if="Object.keys(reservasAgrupadasPorPista).length === 0" class="text-center py-4">
      <p>No tienes reservas actualmente.</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="(pistaReservas, pistaId) in reservasAgrupadasPorPista" :key="pistaId" class="flex flex-col">
        <h2 class="text-xl font-semibold mb-3">{{ getNombrePista(pistaId) }}</h2>
        <div class="flex-grow flex flex-col gap-4">
          <div v-for="reserva in pistaReservas" :key="reserva.id" 
               class="bg-white shadow-md rounded-lg p-4 mb-4 flex flex-col justify-between h-64">
            <div>
              <p class="mb-1">{{ formatDate(reserva.dia) }}</p>
              <p class="mb-1">{{ reserva.hora_inicio }} - {{ reserva.hora_fin }}</p>
              <p v-if="isReservaEnCurso(reserva)" class="text-green-600 font-bold mb-1">En curso</p>
              <ul class="list-disc list-inside overflow-y-auto max-h-24">
                <li v-for="jugador in reserva.jugadores" :key="jugador.id">
                  {{ jugador.name }} {{ jugador.apellido }} ({{ jugador.tipo_jugador }})
                </li>
              </ul>
            </div>
            <div class="mt-2 flex justify-end space-x-2">
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
      datosUsuario: null
    };
  },
  computed: {
    reservasAgrupadasPorPista() {
      const agrupadas = {};
      
      // Primero, separar las reservas en activas y no activas
      const [reservasActivas, reservasNoActivas] = this.reservas.reduce(
        ([activas, noActivas], reserva) => {
          if (this.isReservaEnCurso(reserva)) {
            activas.push(reserva);
          } else {
            noActivas.push(reserva);
          }
          return [activas, noActivas];
        },
        [[], []]
      );

      // Función para agrupar reservas por pista
      const agruparPorPista = (reservas) => {
        reservas.forEach(reserva => {
          // Obtener el ID de la pista de manera segura
          let pistaId = null;
          
          // Primero intentar obtener pista_id directamente
          if (typeof reserva.pista_id !== 'undefined' && reserva.pista_id !== null) {
            pistaId = reserva.pista_id;
          } 
          // Si no existe, intentar obtenerlo del objeto pista
          else if (reserva.pista && typeof reserva.pista.id !== 'undefined') {
            pistaId = reserva.pista.id;
          }
          
          // Si no se pudo obtener un ID válido, usar un ID temporal
          if (pistaId === null) {
            console.warn('Reserva sin ID de pista válido:', reserva);
            pistaId = 'sin-pista';
          }
          
          if (!agrupadas[pistaId]) {
            agrupadas[pistaId] = [];
          }
          agrupadas[pistaId].push(reserva);
        });
      };

      // Primero agregar las reservas activas
      agruparPorPista(reservasActivas);

      // Luego agregar las no activas
      agruparPorPista(reservasNoActivas);

      // Ordenar las reservas de cada pista por fecha y hora
      Object.keys(agrupadas).forEach(pistaId => {
        agrupadas[pistaId].sort((a, b) => {
          const dateA = new Date(a.dia + 'T' + a.hora_inicio);
          const dateB = new Date(b.dia + 'T' + b.hora_inicio);
          return dateA - dateB;
        });
      });

      return agrupadas;
    }
  },
  methods: {
    async fetchMisReservas() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        // Primero obtener los datos del socio actual
        const tokenResponse = await axios.get('http://192.168.10.21:8000/socios/me', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const socioActual = tokenResponse.data;

        // Obtener todas las reservas
        const reservasResponse = await axios.get('http://192.168.10.21:8000/reservas/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });

        console.log('Todas las reservas:', reservasResponse.data);

        // Filtrar las reservas donde el socio actual es jugador
        this.reservas = reservasResponse.data.filter(reserva => {
          // Verificar si el socio actual es jugador
          const esSocioJugador = reserva.jugadores.some(jugador => 
            jugador.name === socioActual.name && 
            jugador.apellido === socioActual.lastname
          );

          if (!esSocioJugador) return false;

          const ahora = new Date();
          const fechaReserva = new Date(reserva.dia);
          
          // Crear fecha/hora de inicio
          const horaInicioArr = reserva.hora_inicio.split(':').map(Number);
          const horaInicio = new Date(fechaReserva);
          horaInicio.setHours(horaInicioArr[0], horaInicioArr[1], 0);

          // Crear fecha/hora de fin
          const horaFinArr = reserva.hora_fin.split(':').map(Number);
          const horaFin = new Date(fechaReserva);
          horaFin.setHours(horaFinArr[0], horaFinArr[1], 0);

          // Si la hora de fin es 00:00 o menor que la hora de inicio, ajustar al día siguiente
          if (horaFin <= horaInicio || (horaFinArr[0] === 0 && horaFinArr[1] === 0)) {
            horaFin.setDate(horaFin.getDate() + 1);
          }

          console.log('Analizando reserva:', {
            dia: reserva.dia,
            inicio: reserva.hora_inicio,
            fin: reserva.hora_fin,
            horaInicioObj: horaInicio,
            horaFinObj: horaFin,
            ahora: ahora
          });

          // Verificar si la reserva está en curso
          const reservaEnCurso = ahora >= horaInicio && ahora <= horaFin;
          if (reservaEnCurso) {
            console.log('Reserva en curso');
            return true;
          }

          // Para reservas futuras, comprobar solo la hora de inicio
          const HORAS_FUTURAS = 24;
          const tiempoLimite = new Date(ahora.getTime() + (HORAS_FUTURAS * 60 * 60 * 1000));
          
          // Mostrar si la hora de inicio está en las próximas 24 horas
          const debeIncluirse = horaInicio >= ahora && horaInicio <= tiempoLimite;
          console.log('¿Debe incluirse?', debeIncluirse, {
            horaInicio: horaInicio,
            ahora: ahora,
            tiempoLimite: tiempoLimite
          });
          
          return debeIncluirse;
        });

        console.log('Reservas filtradas:', this.reservas);

        // Asegurarse de que cada reserva tenga la información de la pista
        await this.fetchPistas();
        
        // Normalizar los datos de las reservas
        this.reservas = this.reservas.map(reserva => {
          let pistaId = null;
          
          if (typeof reserva.pista_id !== 'undefined' && reserva.pista_id !== null) {
            pistaId = reserva.pista_id;
          } else if (reserva.pista && typeof reserva.pista.id !== 'undefined') {
            pistaId = reserva.pista.id;
          }
          
          return {
            ...reserva,
            pista_id: pistaId || 'sin-pista'
          };
        });

      } catch (error) {
        console.error('Error al obtener las reservas:', error);
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

    isReservaEnCurso(reserva) {
      const ahora = new Date();
      const fechaReserva = new Date(reserva.dia);
      
      // Crear fecha/hora de inicio
      const horaInicioArr = reserva.hora_inicio.split(':').map(Number);
      const horaInicio = new Date(fechaReserva);
      horaInicio.setHours(horaInicioArr[0], horaInicioArr[1], 0);

      // Crear fecha/hora de fin
      const horaFinArr = reserva.hora_fin.split(':').map(Number);
      const horaFin = new Date(fechaReserva);
      horaFin.setHours(horaFinArr[0], horaFinArr[1], 0);

      // Si la hora de fin es 00:00 o menor que la hora de inicio, ajustar al día siguiente
      if (horaFin <= horaInicio || (horaFinArr[0] === 0 && horaFinArr[1] === 0)) {
        horaFin.setDate(horaFin.getDate() + 1);
      }

      return ahora >= horaInicio && ahora <= horaFin;
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
          await axios.delete(`http://192.168.10.21:8000/reservas/${reservaId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          await this.fetchMisReservas();
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
        const response = await axios.get('http://192.168.10.21:8000/pistas/');
        this.pistas = response.data.reduce((acc, pista) => {
          acc[pista.id] = pista.name;
          return acc;
        }, {});
      } catch (error) {
        console.error('Error al obtener las pistas:', error);
        this.errorMessage = 'Error al cargar las pistas. Por favor, intente más tarde.';
      }
    }
  },
  async mounted() {
    await this.fetchPistas();
    await this.fetchMisReservas();
  }
};
</script>