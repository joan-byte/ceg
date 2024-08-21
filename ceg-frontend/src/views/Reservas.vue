<template>
  <div class="form-container">
    <h1 class="text-3xl font-bold mb-6">Reserva Pista</h1>

    <form @submit.prevent="handleSubmit">
      <!-- Primera fila: Selección de pista y fecha -->
      <div class="flex mb-4">
        <div class="w-1/2 pr-2">
          <label for="pista" class="block text-gray-700">Elige Pista:</label>
          <select v-model="reserva.pista_id" id="pista" name="pista" class="w-full p-2 border rounded" required>
            <option value="" disabled selected>Elige una opción</option>
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
      <div v-for="(jugador, index) in jugadoresFormateados" :key="index" class="flex mb-4">
        <div class="w-1/3 pr-2">
          <label :for="'jugador' + index + '_name'" class="block text-gray-700">Nombre Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_name'" :name="'jugador' + index + '_name'" v-model="jugador.name" @blur="verificarJugador(index)" placeholder="Nombre" class="w-full p-2 border rounded" :disabled="index >= jugadoresRequeridos">
        </div>
        <div class="w-1/3 px-2">
          <label :for="'jugador' + index + '_apellido'" class="block text-gray-700">Apellido Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_apellido'" :name="'jugador' + index + '_apellido'" v-model="jugador.apellido" @blur="verificarJugador(index)" placeholder="Apellido" class="w-full p-2 border rounded" :disabled="index >= jugadoresRequeridos">
        </div>
        <div class="w-1/3 pl-2">
          <label :for="'jugador' + index + '_tipo'" class="block text-gray-700">Tipo de Jugador {{ index + 1 }}:</label>
          <input type="text" :id="'jugador' + index + '_tipo'" :name="'jugador' + index + '_tipo'" v-model="jugador.tipo_jugador" class="w-full p-2 border rounded" readonly>
        </div>
      </div>

      <!-- Botones -->
      <div class="flex justify-between">
        <button type="submit" class="bg-blue-500 text-white p-2 rounded w-full mr-2">Guardar</button>
        <button type="button" @click="handleReset" class="bg-gray-500 text-white p-2 rounded w-full">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import '../styles/reservas.css';

export default {
  data() {
    return {
      pistas: [], // Lista de pistas
      reserva: {
        pista_id: '',
        dia: '',
        hora_inicio: '',
        hora_fin: '',
        individuales: false
      },
      jugadores: [
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' }
      ],
      jugadoresRequeridos: 4
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
  'reserva.pista_id': function(newVal) {
    if (newVal) {
      this.reserva.individuales = this.pistaSeleccionada.individuales;
      this.jugadoresRequeridos = this.pistaSeleccionada.individuales ? 4 : 4; // Siempre 4 inputs, pero permitimos 2 o 4 jugadores para pistas individuales
      this.ajustarJugadores();
    }
  }
},
  methods: {
    async fetchPistas() {
      try {
        const response = await axios.get('http://localhost:8000/pistas/');
        this.pistas = response.data;
      } catch (error) {
        console.error("Error al obtener las pistas:", error);
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
      }
    },
    async verificarJugador(index) {
      const jugador = this.jugadores[index];
      if (jugador.name && jugador.apellido) {
        try {
          const response = await axios.post('http://localhost:8000/jugadores/verificar/', {
            name: jugador.name,
            apellido: jugador.apellido,
          });
          jugador.tipo_jugador = response.data;
        } catch (error) {
          console.error("Error al verificar el jugador:", error);
          jugador.tipo_jugador = 'Error';
        }
      }
    },
    ajustarJugadores() {
  while (this.jugadores.length < 4) {
    this.jugadores.push({ name: '', apellido: '', tipo_jugador: '' });
  }
  this.jugadores = this.jugadores.slice(0, 4);
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
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' },
        { name: '', apellido: '', tipo_jugador: '' }
      ];
      this.jugadoresRequeridos = 4;
    },
    async handleSubmit() {
  const tieneSocio = this.jugadores.some(jugador => jugador.tipo_jugador && jugador.tipo_jugador !== 'No Socio');
  if (!tieneSocio) {
    alert("Debe haber al menos un jugador socio para realizar la reserva.");
    return;
  }

  const jugadoresCompletos = this.jugadores.filter(j => j.name && j.apellido);

  if (this.pistaSeleccionada.individuales) {
    if (jugadoresCompletos.length !== 2 && jugadoresCompletos.length !== 4) {
      alert("Para una pista individual, debe haber 2 o 4 jugadores completos.");
      return;
    }
  } else {
    if (jugadoresCompletos.length !== 4) {
      alert("Para una pista no individual, debe haber exactamente 4 jugadores completos.");
      return;
    }
  }

  const reservaData = {
    ...this.reserva,
    jugadores: this.jugadores.map(jugador => ({
      name: jugador.name,
      apellido: jugador.apellido,
      tipo_jugador: jugador.tipo_jugador
    }))
  };

  console.log("Datos a enviar:", JSON.stringify(reservaData, null, 2));

  try {
    const response = await axios.post('http://localhost:8000/reservas/', reservaData);
    console.log("Respuesta del servidor:", response.data);
    alert("Reserva guardada con éxito");
    this.handleReset();
    this.fetchPistas();
  } catch (error) {
    console.error("Error completo:", error);
    if (error.response) {
      console.error("Datos de la respuesta:", error.response.data);
      console.error("Detalle del error:", JSON.stringify(error.response.data.detail, null, 2));
      console.error("Estado de la respuesta:", error.response.status);
      console.error("Cabeceras de la respuesta:", error.response.headers);
    }
    alert("Error al guardar la reserva: " + (error.response?.data?.detail ? JSON.stringify(error.response.data.detail) : error.message));
  }
},
  },
  mounted() {
    this.fetchPistas();
  }
};
</script>

<style scoped>
/* Estilos adicionales si los necesitas */
</style>