<template>
  <div class="form-container">
    <h1 class="text-3xl font-bold mb-6">{{ isEditing ? 'Modificar Reserva' : 'Reserva Pista' }}</h1>

    <form @submit.prevent="handleSubmit">
      <!-- Primera fila: Selección de pista y fecha -->
      <div class="flex mb-4">
        <div class="w-1/2 pr-2">
          <label for="pista" class="block text-gray-700">Elige Pista:</label>
          <select v-model="reserva.pista_id" id="pista" name="pista" class="w-full p-2 border rounded" required>
            <option value="" disabled>Elige una opción</option>
            <option v-for="pista in pistas" :key="pista.id" :value="pista.id">
              {{ pista.name }}
            </option>
          </select>
        </div>
        <div class="w-1/2 pl-2">
          <label for="fecha" class="block text-gray-700">Fecha de Inicio:</label>
          <input type="date" id="fecha" name="fecha" v-model="reserva.dia" class="w-full p-2 border rounded" required>
        </div>
      </div>

      <!-- Segunda fila: Hora de inicio y fin -->
      <div class="flex mb-4">
        <div class="w-1/2 pr-2">
          <label for="hora_inicio" class="block text-gray-700">Hora de Inicio:</label>
          <input type="time" id="hora_inicio" name="hora_inicio" v-model="reserva.hora_inicio" @change="calcularHoraFin" class="w-full p-2 border rounded" required>
        </div>
        <div class="w-1/2 pl-2">
          <label for="hora_fin" class="block text-gray-700">Hora de Fin:</label>
          <input type="time" id="hora_fin" name="hora_fin" v-model="reserva.hora_fin" class="w-full p-2 border rounded" readonly>
        </div>
      </div>

      <!-- Filas para cada jugador -->
      <div v-for="(jugador, index) in jugadores" :key="index" class="flex mb-4">
        <div class="w-1/3 pr-2">
          <label :for="'jugador' + index + '_name'" class="block text-gray-700">Nombre Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_name'" :name="'jugador' + index + '_name'" 
                 v-model="jugador.name" @blur="verificarJugador(index)" placeholder="Nombre" 
                 class="w-full p-2 border rounded" :readonly="index === 0 && jugador.readonly">
        </div>
        <div class="w-1/3 px-2">
          <label :for="'jugador' + index + '_apellido'" class="block text-gray-700">Apellido Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_apellido'" :name="'jugador' + index + '_apellido'" 
                 v-model="jugador.apellido" @blur="verificarJugador(index)" placeholder="Apellido" 
                 class="w-full p-2 border rounded" :readonly="index === 0 && jugador.readonly">
        </div>
        <div class="w-1/3 pl-2">
          <label :for="'jugador' + index + '_tipo'" class="block text-gray-700">Tipo de Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_tipo'" :name="'jugador' + index + '_tipo'" 
                 v-model="jugador.tipo_jugador" class="w-full p-2 border rounded" readonly>
        </div>
      </div>

      <!-- Botones -->
      <div class="flex justify-between">
        <button type="submit" class="bg-blue-500 text-white p-2 rounded w-full mr-2">
          {{ isEditing ? 'Modificar' : 'Guardar' }}
        </button>
        <button type="button" @click="handleCancel" class="bg-gray-500 text-white p-2 rounded w-full">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import '../styles/reservas.css';
import { useRouter, useRoute } from 'vue-router';

export default {
  name: 'Reservas',
  setup() {
    const router = useRouter();
    const route = useRoute();
    return { router, route };
  },
  data() {
    return {
      isEditing: false,
      reservaId: null,
      pistas: [],
      reserva: {
        pista_id: '',
        dia: '',
        hora_inicio: '',
        hora_fin: '',
        individuales: false
      },
      jugadores: [
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false }
      ],
      errores: [],
      isAdmin: false,
      userRole: localStorage.getItem('userRole') || '',
      socioActual: null
    };
  },
  computed: {
    jugadoresFormateados() {
      return this.jugadores;
    },
    pistaSeleccionada() {
      return this.pistas.find(p => p.id === this.reserva.pista_id);
    }
  },
  watch: {
    'reserva.pista_id': {
      handler(newVal) {
        console.log('Pista seleccionada:', newVal);
        // Aquí puedes añadir lógica adicional si es necesario
      },
      immediate: true
    }
  },
  methods: {
    async fetchPistas() {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
        this.pistas = response.data;
      } catch (error) {
        console.error("Error al obtener las pistas:", error);
        this.errores.push("Error al obtener las pistas");
      }
    },
    calcularHoraFin() {
      const pistaSeleccionada = this.pistas.find(p => p.id === this.reserva.pista_id);
      if (pistaSeleccionada && this.reserva.hora_inicio) {
        const [hours, minutes] = this.reserva.hora_inicio.split(':').map(Number);
        const tiempoJuego = pistaSeleccionada.tiempo_juego;
        const fin = new Date();
        fin.setHours(hours);
        fin.setMinutes(minutes + tiempoJuego);
        this.reserva.hora_fin = fin.toTimeString().slice(0, 5);
      } else {
        console.error("Hora de inicio no válida o pista no seleccionada");
        this.errores.push("Hora de inicio no válida o pista no seleccionada");
      }
    },
    async verificarJugador(index) {
      console.log('Verificando jugador:', index);
      const jugador = this.jugadores[index];
      console.log('Datos del jugador antes de verificar:', jugador);

      if (jugador.name && jugador.apellido && !jugador.tipo_jugador) {
        try {
          console.log('Enviando solicitud al servidor...');
          const response = await axios.post('http://localhost:8000/jugadores/verificar/', {
            name: jugador.name,
            apellido: jugador.apellido,
          });
          console.log('Respuesta del servidor:', response.data);

          if (typeof response.data === 'object' && 'es_socio' in response.data) {
            // Nueva estructura de respuesta
            jugador.tipo_jugador = response.data.es_socio ? response.data.tipo_socio : "No Socio";
          } else {
            // Estructura de respuesta anterior
            jugador.tipo_jugador = response.data;
          }
        } catch (error) {
          console.error("Error al verificar el jugador:", error);
          jugador.tipo_jugador = 'Error';
          this.errores.push(`Error al verificar el jugador ${jugador.name} ${jugador.apellido}`);
        }
      }

      console.log('Datos del jugador después de verificar:', jugador);
    },
    handleReset() {
      this.reserva = {
        pista_id: '',
        dia: '',
        hora_inicio: '',
        hora_fin: '',
        individuales: false
      };
      this.jugadores = [
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false }
      ];
      this.errores = [];
      this.rellenarDatosPrimerJugador();
    },
    handleCancel() {
      this.handleReset();
      this.router.push('/');
    },
    verificarJugadoresRepetidos() {
      const jugadoresCompletos = this.jugadores.filter(j => j.name && j.apellido);
      const jugadoresUnicos = new Set(jugadoresCompletos.map(j => `${j.name.toLowerCase()} ${j.apellido.toLowerCase()}`));
      return jugadoresUnicos.size !== jugadoresCompletos.length ? "Hay jugadores repetidos en la reserva." : null;
    },
    verificarTiempoReserva() {
      if (this.isEditing) return null;
      const ahora = new Date();
      const fechaReserva = new Date(`${this.reserva.dia}T${this.reserva.hora_inicio}`);
      const diferenciaTiempo = fechaReserva - ahora;
      const horasDiferencia = diferenciaTiempo / (1000 * 60 * 60);
      return (horasDiferencia < 0 || horasDiferencia > 24) ? "Las reservas solo se pueden hacer entre ahora y las próximas 24 horas." : null;
    },
    async verificarSolapamientoJugador(jugador) {
      try {
        const horaInicio = this.reserva.hora_inicio.slice(0, 5);  // Asegura formato HH:MM
        const horaFin = this.reserva.hora_fin.slice(0, 5);  // Asegura formato HH:MM
        const response = await axios.get(`http://localhost:8000/reservas/verificar_solapamiento_jugador/`, {
          params: {
            nombre: jugador.name,
            apellido: jugador.apellido,
            dia: this.reserva.dia,
            hora_inicio: horaInicio,
            hora_fin: horaFin,
            reserva_id: this.isEditing ? this.reservaId : undefined
          }
        });
        if (response.data.solapamiento) {
          return response.data.mensaje;
        }
      } catch (error) {
        console.error("Error al verificar solapamiento de jugador:", error);
        if (error.response && error.response.data) {
          return `Error al verificar solapamiento: ${error.response.data.detail || error.message}`;
        } else {
          return "Error de conexión al verificar solapamiento de jugadores.";
        }
      }
      return null;
    },
    async verificarSolapamientoPista() {
      try {
        const horaInicio = this.reserva.hora_inicio.slice(0, 5);  // Asegura formato HH:MM
        const horaFin = this.reserva.hora_fin.slice(0, 5);  // Asegura formato HH:MM
        const response = await axios.get(`http://localhost:8000/reservas/verificar_solapamiento_pista/`, {
          params: {
            pista_id: this.reserva.pista_id,
            dia: this.reserva.dia,
            hora_inicio: horaInicio,
            hora_fin: horaFin,
            reserva_id: this.isEditing ? this.reservaId : undefined
          }
        });
        if (response.data.solapamiento) {
          return response.data.mensaje;
        }
        return null;
      } catch (error) {
        console.error("Error al verificar solapamiento de pista:", error);
        if (error.response && error.response.data) {
          return `Error al verificar disponibilidad: ${error.response.data.detail || error.message}`;
        } else {
          return "Error al verificar disponibilidad de la pista.";
        }
      }
    },
    async handleSubmit() {
      this.errores = [];

      const errorJugadoresRepetidos = this.verificarJugadoresRepetidos();
      if (errorJugadoresRepetidos) {
        this.errores.push(errorJugadoresRepetidos);
      }

      const errorTiempoReserva = this.verificarTiempoReserva();
      if (errorTiempoReserva) {
        this.errores.push(errorTiempoReserva);
      }

      for (const jugador of this.jugadores) {
        if (jugador.name && jugador.apellido) {
          const errorSolapamientoJugador = await this.verificarSolapamientoJugador(jugador);
          if (errorSolapamientoJugador) {
            this.errores.push(errorSolapamientoJugador);
          }
        }
      }

      const errorSolapamientoPista = await this.verificarSolapamientoPista();
      if (errorSolapamientoPista) {
        this.errores.push(errorSolapamientoPista);
      }

      const tieneSocio = this.jugadores.some(jugador => jugador.tipo_jugador && jugador.tipo_jugador !== 'No Socio');
      if (!tieneSocio) {
        this.errores.push("Debe haber al menos un jugador socio para realizar la reserva.");
      }

      const jugadoresCompletos = this.jugadores.filter(j => j.name && j.apellido);

      if (this.pistaSeleccionada.individuales) {
        if (jugadoresCompletos.length !== 2 && jugadoresCompletos.length !== 4) {
          this.errores.push("Para una pista que permite individuales, debe haber 2 o 4 jugadores completos.");
        }
      } else {
        if (jugadoresCompletos.length !== 4) {
          this.errores.push("Para una pista que no permite individuales, debe haber exactamente 4 jugadores completos.");
        }
      }

      if (this.errores.length > 0) {
        alert(this.errores.join("\n"));
        return;
      }

      console.log('Datos de la reserva antes de enviar:', JSON.stringify(this.reserva, null, 2));
      console.log('Datos de los jugadores antes de enviar:', JSON.stringify(this.jugadores, null, 2));

      const reservaData = {
        ...this.reserva,
        individuales: this.pistaSeleccionada.individuales, // Asegúrate de que este valor sea correcto
        jugadores: jugadoresCompletos.map(jugador => ({
          name: jugador.name,
          apellido: jugador.apellido,
          tipo_jugador: jugador.tipo_jugador
        }))
      };

      console.log('Datos a enviar al backend:', JSON.stringify(reservaData, null, 2));

      try {
        let response;
        const esMiReserva = this.route.name === 'EditarMiReserva';
        
        if (this.isEditing) {
          if (esMiReserva) {
            response = await axios.put(`http://localhost:8000/reservas/mis-reservas/${this.reservaId}`, reservaData, {
              headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });
          } else {
            response = await axios.put(`http://localhost:8000/reservas/${this.reservaId}`, reservaData);
          }
        } else {
          response = await axios.post('http://localhost:8000/reservas/', reservaData);
        }
        console.log("Respuesta del servidor:", response.data);
        console.log("Jugadores actualizados:", response.data.jugadores);

        this.reserva = {
          pista_id: response.data.pista_id,
          dia: response.data.dia,
          hora_inicio: response.data.hora_inicio.slice(0, 5),
          hora_fin: response.data.hora_fin.slice(0, 5),
          individuales: response.data.individuales
        };
        this.jugadores = response.data.jugadores.map(j => ({
          name: j.name,
          apellido: j.apellido,
          tipo_jugador: j.tipo_jugador
        }));

        while (this.jugadores.length < 4) {
          this.jugadores.push({ name: '', apellido: '', tipo_jugador: '' });
        }

        alert(this.isEditing ? "Reserva modificada con éxito" : "Reserva guardada con éxito");
        
        setTimeout(() => {
          this.handleReset();
          if (esMiReserva) {
            this.router.push('/mis-reservas');
          } else {
            this.router.push('/');
          }
        }, 500);
      } catch (error) {
        console.error("Error completo:", error);
        if (error.response) {
          console.error("Datos de la respuesta:", error.response.data);
          console.error("Detalle del error:", JSON.stringify(error.response.data.detail, null, 2));
          console.error("Estado de la respuesta:", error.response.status);
          console.error("Cabeceras de la respuesta:", error.response.headers);
        }
        alert("Error al " + (this.isEditing ? "modificar" : "guardar") + " la reserva: " + (error.response?.data?.detail ? JSON.stringify(error.response.data.detail) : error.message));
      }
    },
    async cargarReserva(id) {
      try {
        const response = await axios.get(`http://localhost:8000/reservas/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const reservaData = response.data;
        this.configurarReservaParaEdicion({
          ...reservaData,
          pista: { id: reservaData.pista_id } // Aseguramos que pista.id esté disponible
        });
      } catch (error) {
        console.error("Error al cargar la reserva:", error);
        alert("Error al cargar la reserva. Por favor, intente nuevamente.");
        this.router.push('/');
      }
    },
    async obtenerSocioActual() {
      const token = localStorage.getItem('token');
      if (token && this.userRole === 'socio') {
        try {
          const response = await axios.get('http://localhost:8000/socios/me', {
            headers: { Authorization: `Bearer ${token}` }
          });
          console.log('Datos del socio recibidos:', response.data);
          this.socioActual = response.data;
          this.rellenarDatosPrimerJugador();
        } catch (error) {
          console.error("Error al obtener datos del socio:", error);
        }
      }
    },
    rellenarDatosPrimerJugador() {
      console.log('Entrando en rellenarDatosPrimerJugador');
      console.log('socioActual:', this.socioActual);
      console.log('isEditing:', this.isEditing);
      if (this.socioActual && !this.isEditing) {
        console.log('Rellenando datos del primer jugador');
        const jugador = {
          name: this.socioActual.name,
          apellido: this.socioActual.lastname,
          tipo_jugador: this.socioActual.type,
          readonly: true
        };
        console.log('Datos del jugador antes de asignar:', jugador);
        this.jugadores[0] = jugador;
        console.log('Datos del primer jugador después de rellenar:', this.jugadores[0]);
        this.verificarJugador(0);
      } else {
        console.log('No se rellenaron los datos del primer jugador');
      }
    },
    async determinarModoEdicion() {
      const id = this.$route.params.id;
      const esMiReserva = this.$route.name === 'EditarMiReserva';
      const esEditarReserva = this.$route.name === 'EditarReserva';

      await this.fetchPistas();

      if (id && (esMiReserva || esEditarReserva)) {
        this.isEditing = true;
        this.reservaId = id;
        if (esMiReserva) {
          await this.cargarMiReserva(id);
        } else {
          await this.cargarReserva(id);
        }
      } else {
        this.resetForm();
        await this.obtenerSocioActual();
      }
    },
    async cargarMiReserva(id) {
      try {
        const response = await axios.get(`http://localhost:8000/reservas/mis-reservas/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.configurarReservaParaEdicion(response.data);
        await this.fetchPistas(); // Asegúrate de que las pistas se carguen
        this.$forceUpdate(); // Fuerza una actualización del componente
      } catch (error) {
        console.error("Error al cargar mi reserva:", error);
        if (error.response && error.response.status === 404) {
          alert("La reserva no fue encontrada. Puede que haya sido eliminada.");
        } else if (error.response && error.response.status === 403) {
          alert("No tienes permiso para ver esta reserva.");
        } else {
          alert("Error al cargar la reserva. Por favor, intente nuevamente.");
        }
        this.router.push('/mis-reservas');
      }
    },
    configurarReservaParaEdicion(reserva) {
      this.reserva = {
        pista_id: reserva.pista.id,
        dia: reserva.dia,
        hora_inicio: reserva.hora_inicio.slice(0, 5),
        hora_fin: reserva.hora_fin.slice(0, 5),
        individuales: reserva.individuales
      };
      this.jugadores = reserva.jugadores.map((j, index) => ({
        name: j.name,
        apellido: j.apellido,
        tipo_jugador: j.tipo_jugador,
        readonly: index === 0
      }));
      while (this.jugadores.length < 4) {
        this.jugadores.push({ name: '', apellido: '', tipo_jugador: '', readonly: false });
      }
      this.isEditing = true;
      this.reservaId = reserva.id;
      console.log('Reserva configurada para edición:', this.reserva);
    },
    resetForm() {
      this.reserva = {
        pista_id: '',
        dia: '',
        hora_inicio: '',
        hora_fin: '',
        individuales: false
      };
      this.jugadores = [
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false },
        { name: '', apellido: '', tipo_jugador: '', readonly: false }
      ];
      this.isEditing = false;
      this.reservaId = null;
    }
  },
  mounted() {
    this.$nextTick(async () => {
      await this.fetchPistas();
      await this.determinarModoEdicion();
    });
  }
};
</script>

<style scoped>
/* Puedes añadir estilos específicos aquí si los necesitas */
</style>